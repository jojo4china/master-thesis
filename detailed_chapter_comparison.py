#!/usr/bin/env python3
import docx2txt
import re

def extract_chapters_with_content(lines):
    """提取章节及其内容"""
    chapters = []
    current_chapter = None
    current_content = []
    
    for i, line in enumerate(lines):
        # 检测章节标题（简化版检测）
        if '第' in line and '章' in line and len(line.strip()) < 100:
            # 保存当前章节
            if current_chapter:
                chapters.append({
                    'title': current_chapter['title'],
                    'line_start': current_chapter['line_start'],
                    'line_end': i - 1,
                    'content': current_content.copy(),
                    'word_count': sum(len(content.split()) for content in current_content if content.strip())
                })
            
            # 开始新章节
            current_chapter = {
                'title': line.strip(),
                'line_start': i,
                'line_end': i
            }
            current_content = [line]
        else:
            if current_chapter:
                current_content.append(line)
                current_chapter['line_end'] = i
    
    # 添加最后一个章节
    if current_chapter:
        chapters.append({
            'title': current_chapter['title'],
            'line_start': current_chapter['line_start'],
            'line_end': current_chapter['line_end'],
            'content': current_content.copy(),
            'word_count': sum(len(content.split()) for content in current_content if content.strip())
        })
    
    return chapters

def analyze_document_structure():
    print("🔍 正在详细分析文档结构差异...")
    
    # 读取两个文档
    original = docx2txt.process('硕士论文1_原始备份.docx', None)
    modified = docx2txt.process('硕士论文1_修改版.docx', None)
    
    original_lines = original.split('\n')
    modified_lines = modified.split('\n')
    
    print(f"📏 原始备份: {len(original_lines)} 行, {len(original)} 字符")
    print(f"📏 修改版: {len(modified_lines)} 行, {len(modified)} 字符")
    
    # 提取章节
    original_chapters = extract_chapters_with_content(original_lines)
    modified_chapters = extract_chapters_with_content(modified_lines)
    
    print(f"\n📖 章节结构对比:")
    print(f"   原始备份: {len(original_chapters)} 章")
    print(f"   修改版: {len(modified_chapters)} 章")
    
    print("\n" + "="*60)
    print("📋 详细章节对比")
    print("="*60)
    
    # 显示原始备份章节
    print("\n📚 原始备份章节结构:")
    for i, chapter in enumerate(original_chapters, 1):
        print(f"   {i}. {chapter['title']} (行 {chapter['line_start']+1}-{chapter['line_end']+1}, 约 {chapter['word_count']} 字)")
    
    print("\n📚 修改版章节结构:")
    for i, chapter in enumerate(modified_chapters, 1):
        print(f"   {i}. {chapter['title']} (行 {chapter['line_start']+1}-{chapter['line_end']+1}, 约 {chapter['word_count']} 字)")
    
    # 对比章节变化
    original_titles = [ch['title'] for ch in original_chapters]
    modified_titles = [ch['title'] for ch in modified_chapters]
    
    removed = set(original_titles) - set(modified_titles)
    added = set(modified_titles) - set(original_titles)
    common = set(original_titles) & set(modified_titles)
    
    print(f"\n🔍 章节变化统计:")
    print(f"   保留章节: {len(common)}")
    print(f"   删除章节: {len(removed)}")
    print(f"   新增章节: {len(added)}")
    
    if removed:
        print(f"\n❌ 删除的章节:")
        for chapter in removed:
            # 找到原始备份中该章节的详细信息
            orig_chapter = next((ch for ch in original_chapters if ch['title'] == chapter), None)
            if orig_chapter:
                print(f"   - {chapter} (约 {orig_chapter['word_count']} 字)")
    
    if added:
        print(f"\n➕ 新增的章节:")
        for chapter in added:
            # 找到修改版中该章节的详细信息
            mod_chapter = next((ch for ch in modified_chapters if ch['title'] == chapter), None)
            if mod_chapter:
                print(f"   + {chapter} (约 {mod_chapter['word_count']} 字)")
    
    # 分析共同章节的内容变化
    print(f"\n📊 共同章节内容对比:")
    for common_title in common:
        orig_chapter = next((ch for ch in original_chapters if ch['title'] == common_title), None)
        mod_chapter = next((ch for ch in modified_chapters if ch['title'] == common_title), None)
        
        if orig_chapter and mod_chapter:
            word_change = mod_chapter['word_count'] - orig_chapter['word_count']
            print(f"   {common_title}: {orig_chapter['word_count']} → {mod_chapter['word_count']} 字符 ({word_change:+})")
    
    # 查找关键内容变化
    print(f"\n🎯 关键内容分析:")
    
    # 检查是否有特殊章节内容
    special_sections = ['摘要', '关键词', '参考文献', '致谢', '攻读博士学位期间论文发表情况']
    
    for section in special_sections:
        orig_count = original.count(section)
        mod_count = modified.count(section)
        if orig_count != mod_count:
            print(f"   '{section}': {orig_count} → {mod_count} ({mod_count-orig_count:+})")
    
    # 分析文档开头和结尾
    print(f"\n📄 文档开头对比:")
    print(f"   原始备份开头5行:")
    for i, line in enumerate(original_lines[:5]):
        print(f"     {i+1}: {line[:100]}...")
    
    print(f"   修改版开头5行:")
    for i, line in enumerate(modified_lines[:5]):
        print(f"     {i+1}: {line[:100]}...")
    
    print(f"\n📄 文档结尾对比:")
    print(f"   原始备份结尾5行:")
    for i, line in enumerate(original_lines[-5:], len(original_lines)-4):
        print(f"     {i}: {line[:100]}...")
    
    print(f"   修改版结尾5行:")
    for i, line in enumerate(modified_lines[-5:], len(modified_lines)-4):
        print(f"     {i}: {line[:100]}...")

if __name__ == "__main__":
    analyze_document_structure()