'''
01 - Feature Engineering: Feature Extraction
'''

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import jieba

# 1. Dictionary Feature Extraction
def dict_demo():
    # Input data
    data = [
        {'city': 'Beijing', 'temperature': 100},
        {'city': 'Shanghai', 'temperature': 60},
        {'city': 'Shenzhen', 'temperature': 30}
    ]

    # Initialize and transform
    transfer = DictVectorizer(sparse=False)
    trans_data = transfer.fit_transform(data)

    # Output results
    print("Feature names:\n", transfer.get_feature_names_out())
    print("Transformed data:\n", trans_data)

dict_demo()

# 2. Text Feature Extraction - English
def english_count_text_demo():
    data = [
        "life is short, I like python",
        "life is too long, I dislike python"
    ]

    transfer = CountVectorizer(stop_words=['dislike'])
    transfer_data = transfer.fit_transform(data)

    print("Feature names:\n", transfer.get_feature_names_out())
    print("Transformed data:\n", transfer_data.toarray())

english_count_text_demo()

# 3. Text Feature Extraction - Chinese
def cut_word(text):
    return " ".join(list(jieba.cut(text)))

def chinese_count_text_demo():
    data = [
        "人生 苦短，我 喜欢 Python",
        "生活 太长久，我 不 喜欢 Python"
    ]

    transfer = CountVectorizer()
    transfer_data = transfer.fit_transform(data)

    print("Feature names:\n", transfer.get_feature_names_out())
    print("Transformed data:\n", transfer_data.toarray())

chinese_count_text_demo()

# 4. Text Feature Extraction - Chinese 2 (with stop words and segmenting)
def chinese_count_text_demo2():
    data = [
        "生命的每一个瞬间， 都只有一次， 不会重来！珍惜所有的快乐和忧伤；",
        "认识你就输。可是，不认真你就废了！",
        "不耻长，秋无所获！晨不惜时，日无所为！少不勤勉，老无所归！莫负自己！"
    ]

    # Segment each sentence
    segmented = [cut_word(sentence) for sentence in data]
    print("Segmented:\n", segmented)

    transfer = CountVectorizer(
        stop_words=['一次', '废了', '输了']
    )
    transfer_data = transfer.fit_transform(segmented)

    print("Feature names:\n", transfer.get_feature_names_out())
    print("Transformed data:\n", transfer_data.toarray())

chinese_count_text_demo2()

# 5. Text Feature Extraction - Chinese 3 (TF-IDF)
def tfidf_text_demo():
    data = [
        "人生苦短,我喜欢Python",
        "生活太长久,我不喜欢Python"
    ]

    segmented = [cut_word(text) for text in data]
    print("Segmented:\n", segmented)

    transfer = TfidfVectorizer()
    transfer_data = transfer.fit_transform(segmented)

    print("Feature names:\n", transfer.get_feature_names_out())
    print("TF-IDF result:\n", transfer_data.toarray())

tfidf_text_demo()
