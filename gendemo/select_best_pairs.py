#!/usr/bin/env python3
"""
从 clap_detailed_results.csv 中选出 CLAP 提升最大的 20 对
复制到 /apdcephfs/share_303556863/ggyzhang/zheqid/demo/editdemo
"""

import pandas as pd
import shutil
import os
from pathlib import Path

# 配置路径
CSV_PATH = "/apdcephfs/share_303556863/ggyzhang/zheqid/peaudio/final_eval/semantic_cond/dim64_20260126_140131/clap_detailed_results.csv"
OUTPUT_DIR = "/apdcephfs/share_303556863/ggyzhang/zheqid/demo/editdemo"
TOP_N = 20

def main():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 读取CSV
    df = pd.read_csv(CSV_PATH)
    print(f"总共 {len(df)} 条记录")
    
    # 按 CLAP 提升排序，选择最大的 TOP_N 对
    df_sorted = df.sort_values('laion_clap_improvement', ascending=False)
    top_pairs = df_sorted.head(TOP_N)
    
    print(f"\n选择 CLAP 提升最大的 {TOP_N} 对:")
    print("-" * 80)
    
    # 创建子目录
    original_dir = os.path.join(OUTPUT_DIR, "original_audio")
    edited_dir = os.path.join(OUTPUT_DIR, "edited_audio")
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(edited_dir, exist_ok=True)
    
    # 保存选中的记录到CSV
    captions_data = []
    
    for idx, (_, row) in enumerate(top_pairs.iterrows(), 1):
        audio_id = row['audio_id']
        src_caption = row['src_caption']
        tar_caption = row['tar_caption']
        original_audio = row['original_audio']
        edited_audio = row['edited_audio']
        improvement = row['laion_clap_improvement']
        
        print(f"\n{idx}. {audio_id}")
        print(f"   源: {src_caption}")
        print(f"   目标: {tar_caption}")
        print(f"   CLAP提升: {improvement:.4f}")
        
        # 复制音频文件
        if os.path.exists(original_audio):
            # 使用带编号的文件名避免重复
            original_filename = f"{idx:02d}_{os.path.basename(original_audio)}"
            shutil.copy2(original_audio, os.path.join(original_dir, original_filename))
            print(f"   ✓ 复制原始音频: {original_filename}")
        else:
            print(f"   ✗ 原始音频不存在: {original_audio}")
            original_filename = ""
        
        if os.path.exists(edited_audio):
            edited_filename = f"{idx:02d}_{os.path.basename(edited_audio)}"
            shutil.copy2(edited_audio, os.path.join(edited_dir, edited_filename))
            print(f"   ✓ 复制编辑音频: {edited_filename}")
        else:
            print(f"   ✗ 编辑音频不存在: {edited_audio}")
            edited_filename = ""
        
        # 记录caption信息
        captions_data.append({
            'rank': idx,
            'audio_id': audio_id,
            'src_caption': src_caption,
            'tar_caption': tar_caption,
            'clap_improvement': improvement,
            'original_file': original_filename,
            'edited_file': edited_filename
        })
    
    # 保存caption信息到CSV
    captions_df = pd.DataFrame(captions_data)
    captions_csv = os.path.join(OUTPUT_DIR, "captions.csv")
    captions_df.to_csv(captions_csv, index=False)
    print(f"\n\n✓ Caption信息已保存到: {captions_csv}")
    print(f"✓ 原始音频已复制到: {original_dir}")
    print(f"✓ 编辑音频已复制到: {edited_dir}")

if __name__ == "__main__":
    main()
