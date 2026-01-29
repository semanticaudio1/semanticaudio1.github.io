#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化脚本：
1. 根据audioldm中音频的名字
2. 找到test-audiocaps.tsv中对应的caption
3. 把test_eval/test中对应的GT音频复制到gt文件夹
"""

import os
import shutil
import csv

# 路径配置
DEMO_DIR = "/apdcephfs/share_303556863/ggyzhang/zheqid/demo"
AUDIOLDM_DIR = os.path.join(DEMO_DIR, "audioldm")
GT_OUTPUT_DIR = os.path.join(DEMO_DIR, "gt")
TSV_FILE = "/apdcephfs/share_303556863/ggyzhang/zheqid/data/test-audiocaps.tsv"
GT_SOURCE_DIR = "/apdcephfs/share_303556863/ggyzhang/zheqid/data/test_eval/test"

def main():
    # 创建gt输出文件夹
    os.makedirs(GT_OUTPUT_DIR, exist_ok=True)
    
    # 1. 加载TSV映射 (id -> caption)
    id_to_caption = {}
    with open(TSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # 跳过header
        for row in reader:
            if len(row) >= 2:
                audio_id, caption = row[0], row[1]
                id_to_caption[audio_id] = caption
    print(f"从TSV加载了 {len(id_to_caption)} 条映射")
    
    # 2. 获取audioldm中的音频文件名
    audio_files = [f for f in os.listdir(AUDIOLDM_DIR) if f.endswith('.wav')]
    print(f"audioldm中有 {len(audio_files)} 个音频文件")
    
    # 3. 处理每个音频
    results = []
    for audio_file in audio_files:
        # 提取audio_id (去掉.wav后缀)
        audio_id = audio_file.replace('.wav', '')
        
        # 查找caption
        caption = id_to_caption.get(audio_id, "未找到")
        
        # 复制GT音频
        gt_source = os.path.join(GT_SOURCE_DIR, audio_file)
        gt_dest = os.path.join(GT_OUTPUT_DIR, audio_file)
        
        if os.path.exists(gt_source):
            shutil.copy2(gt_source, gt_dest)
            print(f"✓ {audio_id}: 已复制GT音频, caption: {caption[:50]}...")
        else:
            print(f"✗ {audio_id}: GT音频不存在于 {gt_source}")
        
        results.append({
            'audio_id': audio_id,
            'caption': caption,
            'gt_copied': os.path.exists(gt_source)
        })
    
    # 4. 保存结果到CSV
    output_csv = os.path.join(DEMO_DIR, "captions.csv")
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['audio_id', 'caption', 'gt_copied'])
        writer.writeheader()
        writer.writerows(results)
    print(f"\n结果已保存到: {output_csv}")

if __name__ == "__main__":
    main()
