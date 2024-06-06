import re

# 读取字典文件，用于非单词错误检测
with open('vocab.txt', 'r', encoding='utf-8') as vocab_file:
    vocab = [word.lower() for word in (line.strip() for line in vocab_file)]

def correct_spelling(sentence):
    words = re.findall(r'\b[\w\']+|[-.,、]|[\s]|[.,;!?]', sentence)
    corrected_words = []
    for word in words:
        if re.match(r'\b[\w\']+|[-.,、]', word) and word.lower() not in vocab:
            corrected_word = correction(word)
            # 保持原字母大小写
            if word[0].isupper():
                corrected_word = corrected_word.capitalize()
            if word.isupper():
                corrected_word = corrected_word.upper()
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)
    return ''.join(corrected_words)

def correction(word):
    if word.isalnum():
        candidates = known([word]) or known(edits1(word)) or known(edits2(word)) or [word]
        return candidates[0]
    else:
        return word

def known(words):
    return list(w for w in words if re.match(r'\b[\w\']+|[-.,、]', w) and w.lower() in vocab)

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return list(deletes + transposes + replaces + inserts)

def edits2(word):
    return list(e2 for e1 in edits1(word) for e2 in edits1(e1))

# 读取测试数据文件
with open('testdata.txt', 'r', encoding='utf-8') as testdata_file:
    lines = testdata_file.readlines()

count =0
# 拼写校正并写入结果文件
with open('result.txt', 'w', encoding='utf-8') as result_file:
    for line in lines:
        count+=1
        if count%10==0:
            print(count)
        parts = line.strip().split('\t')
        sentence_id, _, sentence = parts
        corrected_sentence = correct_spelling(sentence)
        result_file.write(f"{sentence_id}\t{corrected_sentence}\n")
