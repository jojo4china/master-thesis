#!/usr/bin/env python3
import docx2txt
from difflib import SequenceMatcher

def compare_original_and_modified():
    print("🔍 正在对比原始备份和修改版的差异...")
    
    # 读取原始备份
    try:
        original = docx2txt.process('硕士论文1_原始备份.docx', None)
        print(f"✅ 原始备份文档加载成功: {len(original)} 字符")
    except Exception as e:
        print(f"❌ 原始备份文档加载失败: {e}")
        return
    
    # 读取修改版
    try:
        modified = docx2txt.process('硕士论文1_修改版.docx', None)
        print(f"✅ 修改版文档加载成功: {len(modified)} 字符")
    except Exception as e:
        print(f"❌ 修改版文档加载失败: {e}")
        return
    
    print("\n" + "="*80)
    print("📊 原始备份 vs 修改版 差异分析")
    print("="*80)
    
    # 基本统计
    original_length = len(original)
    modified_length = len(modified)
    length_diff = modified_length - original_length
    
    print(f"📏 原始备份长度: {original_length:,} 字符")
    print(f"📏 修改版长度: {modified_length:,} 字符")
    print(f"📊 长度差异: {length_diff:+} 字符 ({length_diff/original_length*100:+.2f}%)")
    
    # 计算相似度
    similarity = SequenceMatcher(None, original, modified).ratio()
    print(f"🔍 整体相似度: {similarity:.2%}")
    
    # 按行分析
    original_lines = original.split('\n')
    modified_lines = modified.split('\n')
    
    print(f"\n📝 段落数统计:")
    print(f"   原始备份: {len(original_lines)} 段")
    print(f"   修改版: {len(modified_lines)} 段")
    print(f"   段落数差异: {len(modified_lines) - len(original_lines):+} 段")
    
    # 查找章节差异
    def extract_chapters(lines):
        chapters = []
        for i, line in enumerate(lines):
            if '第' in line and '章' in line and len(line) < 100:
                chapters.append({
                    'title': line.strip(),
                    'line_number': i,
                    'content': line
                })
        return chapters
    
    original_chapters = extract_chapters(original_lines)
    modified_chapters = extract_chapters(modified_lines)
    
    print(f"\n📖 章节对比:")
    print(f"   原始备份: {len(original_chapters)} 章")
    print(f"   修改版: {len(modified_chapters)} 章")
    
    # 对比章节标题
    original_titles = [ch['title'] for ch in original_chapters]
    modified_titles = [ch['title'] for ch in modified_chapters]
    
    removed_chapters = set(original_titles) - set(modified_titles)
    added_chapters = set(modified_titles) - set(original_titles)
    
    if removed_chapters:
        print(f"\n❌ 删除的章节:")
        for chapter in removed_chapters:
            print(f"   - {chapter}")
    
    if added_chapters:
        print(f"\n➕ 新增的章节:")
        for chapter in added_chapters:
            print(f"   + {chapter}")
    
    # 查找前几个段落的差异
    print(f"\n🔍 前20行内容对比:")
    print("-" * 60)
    
    comparison_lines = min(20, len(original_lines), len(modified_lines))
    found_difference = False
    
    for i in range(comparison_lines):
        if i < len(original_lines) and i < len(modified_lines):
            if original_lines[i].strip() != modified_lines[i].strip():
                if not found_difference:
                    print("\n📋 发现差异的行:")
                    found_difference = True
                
                print(f"\n--- 第{i+1}行 ---")
                print(f"原始备份: {original_lines[i][:150]}...")
                print(f"修改版:   {modified_lines[i][:150]}...")
    
    if not found_difference:
        print("前20行内容没有明显差异")
    
    # 查找关键差异
    print(f"\n🎯 关键差异分析:")
    
    # 查找可能的研究内容变化
    research_keywords = ['研究', '分析', '合成', '表征', '磁性', '介电', '结构', '性能']
    
    for keyword in research_keywords:
        original_count = original.count(keyword)
        modified_count = modified.count(keyword)
        if original_count != modified_count:
            print(f"   '{keyword}': {original_count} → {modified_count} ({modified_count-original_count:+})")
    
    # 检查是否有特殊内容
    special_content = ['摘要', '关键词', '结论', '展望', '参考文献']
    for content in special_content:
        orig_has = content in original
        mod_has = content in modified
        if orig_has != mod_has:
            status = '新增' if mod_has else '删除'
            print(f"   '{content}': {status}")

if __name__ == "__main__":
    compare_original_and_modified()