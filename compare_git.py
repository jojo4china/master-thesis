import docx2txt

def compare_documents():
    # 获取原版内容
    try:
        original = docx2txt.process('硕士论文1.docx', None)
        print(f'原版文档加载成功: {len(original)} 字符')
    except Exception as e:
        original = '原版文件已删除或无法读取'
        print(f'原版文档加载失败: {e}')
    
    # 获取修改版内容
    try:
        modified = docx2txt.process('硕士论文1_修改版.docx', None)
        print(f'修改版文档加载成功: {len(modified)} 字符')
    except Exception as e:
        modified = '修改版文件读取失败'
        print(f'修改版文档加载失败: {e}')
    
    print('\n=== 文档差异对比 ===')
    print(f'原版长度: {len(original)} 字符')
    print(f'修改版长度: {len(modified)} 字符')
    print(f'差异: {len(modified) - len(original):+} 字符')
    
    # 查找主要差异
    if isinstance(original, str) and isinstance(modified, str):
        lines_original = original.split('\n')
        lines_modified = modified.split('\n')
        
        print('\n=== 前10行对比 ===')
        for i in range(min(10, len(lines_original), len(lines_modified))):
            if lines_original[i] != lines_modified[i]:
                print(f'行 {i+1}:')
                print(f'  原版: {lines_original[i][:150]}...')
                print(f'  修改版: {lines_modified[i][:150]}...')
                break
        else:
            print('前10行没有明显差异')
        
        # 查找章节差异
        print('\n=== 章节对比 ===')
        original_chapters = [line for line in lines_original if '第' in line and '章' in line]
        modified_chapters = [line for line in lines_modified if '第' in line and '章' in line]
        
        print(f'原版章节数: {len(original_chapters)}')
        print(f'修改版章节数: {len(modified_chapters)}')
        
        if len(original_chapters) != len(modified_chapters):
            print('⚠️ 章节数量发生变化！')
            
            # 查找具体的章节差异
            original_set = set(original_chapters)
            modified_set = set(modified_chapters)
            
            removed = original_set - modified_set
            added = modified_set - original_set
            
            if removed:
                print('❌ 删除的章节:')
                for chapter in removed:
                    print(f'  - {chapter}')
            
            if added:
                print('➕ 新增的章节:')
                for chapter in added:
                    print(f'  + {chapter}')

if __name__ == "__main__":
    compare_documents()