# Decision Tree - ID3 Algorithm Implementation
# 1. Calculate entropy
# 2. Feature selection (information gain)
# 3. Build the tree recursively
# 4. Predict with the tree

from pprint import pprint
import math

# 1. Calculate entropy
def calc_entropy(dataset):
    label_counts = {}
    for record in dataset:
        label = record[-1]
        label_counts[label] = label_counts.get(label, 0) + 1

    entropy = 0
    for count in label_counts.values():
        p = count / len(dataset)
        entropy -= p * math.log2(p)

    return round(entropy, 3)

# 2. Split the dataset based on a feature and its value
def split_dataset(dataset, axis, value):
    result = []
    for row in dataset:
        if row[axis] == value:
            reduced_row = row[:axis] + row[axis + 1:]
            result.append(reduced_row)
    return result

# 3. Choose the best feature (max information gain)
def choose_best_feature(dataset):
    base_entropy = calc_entropy(dataset)
    feature_count = len(dataset[0]) - 1
    best_gain = 0
    best_feature = -1

    for i in range(feature_count):
        feature_values = [row[i] for row in dataset]
        unique_values = set(feature_values)
        new_entropy = 0

        for value in unique_values:
            sub_dataset = split_dataset(dataset, i, value)
            p = len(sub_dataset) / len(dataset)
            new_entropy += p * calc_entropy(sub_dataset)

        gain = base_entropy - new_entropy
        if gain > best_gain:
            best_gain = gain
            best_feature = i

    return best_feature

# 4. Majority voting for leaf node
def majority_vote(class_list):
    result = {}
    for label in class_list:
        result[label] = result.get(label, 0) + 1
    return max(result, key=result.get)

# 5. Build decision tree recursively
def build_tree(dataset, labels):
    class_list = [row[-1] for row in dataset]

    # If all labels are the same, return the label
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # If no more features, return majority class
    if len(dataset[0]) == 1:
        return majority_vote(class_list)

    # Choose the best feature
    best_feat = choose_best_feature(dataset)
    best_label = labels[best_feat]
    tree = {best_label: {}}
    del(labels[best_feat])

    feat_values = [row[best_feat] for row in dataset]
    unique_values = set(feat_values)

    for value in unique_values:
        sub_labels = labels[:]
        subtree = build_tree(split_dataset(dataset, best_feat, value), sub_labels)
        tree[best_label][value] = subtree

    return tree

# 6. Classify with decision tree
def classify(tree, feat_labels, test_vector):
    root = list(tree.keys())[0]
    second_dict = tree[root]
    feat_index = feat_labels.index(root)

    for key in second_dict.keys():
        if test_vector[feat_index] == key:
            if isinstance(second_dict[key], dict):
                class_label = classify(second_dict[key], feat_labels, test_vector)
            else:
                class_label = second_dict[key]
            return class_label

# 7. Load and preprocess dataset
def load_dataset():
    with open("lenses.txt", "r") as f:
        lines = f.readlines()
    dataset = [line.strip().split("\t") for line in lines]
    return dataset

# 8. Train decision tree
def train():
    dataset = load_dataset()
    labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    labels_copy = labels[:]
    tree = build_tree(dataset, labels_copy)
    return tree, labels

# 9. Predict using trained model
def predict(tree, labels, test_vector):
    result = classify(tree, labels, test_vector)
    return result

# Main execution
if __name__ == '__main__':
    tree, labels = train()
    pprint(tree)
    test_sample = ['young', 'myope', 'no', 'reduced']
    result = predict(tree, labels, test_sample)
    print("Prediction:", result)
