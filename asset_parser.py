def count_character_lines(script_text):  #建立统计角色台词数据函数
    '''
    针对出现的角色，统计输入台词的数量。
    Args:
    script_text (str): 包含完整剧本的多行字符串。
     Returns:
        dict: 一个字典，键是角色名，值是台词数。
    '''
#建立初始化容器。
    output_dic = {}
    # 建立接受处理文本后的变量，处理文本方式：换行的列表。
    f_o = script_text.splitlines()
    #建立循环逻辑
    for line in f_o :
        #数据清洗
        line = line.replace(':', '：') # 统一所需符号格式：英文冒替换成中文冒号
        if '：' in line :
            #建立数据容器，并以split函数提取所需key
            cha_name_parts ,cha_dia = line.split('：',1) #1 代表只分第一个：
            #进一步用strip()数据清洗
            cha_name = cha_name_parts.strip()
            #因为剧本格式对数据再一次清洗，变通性不强。
            if '[' not in cha_name:
                #利用get函数赋值
                output_dic[cha_name] = output_dic.get( cha_name,0)+1 
    #输出            
    return  output_dic
   
def filter_major_characters(character_counts, min_lines=3):
    """
    从角色计数字典中，筛选出台词数大于或等于最小阈值的角色。

    Args:
        character_counts (dict): 一个包含角色名和台词数的字典。
        min_lines (int, optional): 最小台词数的阈值。默认为 3。

    Returns:
        dict: 一个只包含主要角色的新字典。
    """
    
    # 使用一行字典推导式，完成筛选和创建新字典的过程。
    # 逻辑: 对于 character_counts 中的每一对 character 和 count，
    #       如果 count 大于或等于 min_lines，
    #       就把这对 {character: count} 放入新字典。
    major_characters_dict = {
        character: count 
        for character, count in character_counts.items() 
        if count >= min_lines
    }
    
    return major_characters_dict




