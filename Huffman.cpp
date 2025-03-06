#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <string>

using namespace std;

class Node {
public:
    char ch;
    int freq;
    Node* left;
    Node* right;

    Node(char character, int frequency) : ch(character), freq(frequency), left(nullptr), right(nullptr) {}

    bool operator<(const Node& other) const {
        return freq > other.freq; // Min-heap based on frequency
    }
};

class MinHeap {
private:
    vector<Node*> heap;

    int parent(int index) { return (index - 1) / 2; }
    int left_child(int index) { return 2 * index + 1; }
    int right_child(int index) { return 2 * index + 2; }

    void _heapify_up(int index) {
        while (index != 0 && heap[parent(index)]->freq > heap[index]->freq) {
            swap(heap[index], heap[parent(index)]);
            index = parent(index);
        }
    }

    void _heapify_down(int index) {
        int smallest = index;
        int left = left_child(index);
        int right = right_child(index);

        if (left < heap.size() && heap[left]->freq < heap[smallest]->freq) {
            smallest = left;
        }

        if (right < heap.size() && heap[right]->freq < heap[smallest]->freq) {
            smallest = right;
        }

        if (smallest != index) {
            swap(heap[index], heap[smallest]);
            _heapify_down(smallest);
        }
    }

public:
    MinHeap() {}

    void insert(Node* node) {
        heap.push_back(node);
        _heapify_up(heap.size() - 1);
    }

    Node* extract_min() {
        if (heap.empty()) {
            return nullptr;
        }
        if (heap.size() == 1) {
            Node* root = heap.back();
            heap.pop_back();
            return root;
        }

        Node* root = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        _heapify_down(0);
        return root;
    }

    bool is_empty() { return heap.empty(); }
    int size() { return heap.size(); }
};

Node* build_huffman_tree(const string& text) {
    unordered_map<char, int> frequency;
    for (char ch : text) {
        frequency[ch]++;
    }

    MinHeap min_heap;
    for (const auto& pair : frequency) {
        min_heap.insert(new Node(pair.first, pair.second));
    }

    while (min_heap.size() > 1) {
        Node* left = min_heap.extract_min();
        Node* right = min_heap.extract_min();
        Node* merged = new Node('\0', left->freq + right->freq);
        merged->left = left;
        merged->right = right;
        min_heap.insert(merged);
    }

    return min_heap.extract_min();
}

void generate_huffman_codes(Node* node, const string& prefix, unordered_map<char, string>& codebook) {
    if (node != nullptr) {
        if (node->ch != '\0') {
            codebook[node->ch] = prefix;
        }
        generate_huffman_codes(node->left, prefix + "0", codebook);
        generate_huffman_codes(node->right, prefix + "1", codebook);
    }
}

pair<unordered_map<char, string>, string> huffman_encoding(const string& text) {
    Node* root = build_huffman_tree(text);
    unordered_map<char, string> huffman_codes;
    generate_huffman_codes(root, "", huffman_codes);

    string encoded_text;
    for (char ch : text) {
        encoded_text += huffman_codes[ch];
    }

    return {huffman_codes, encoded_text};
}

string huffman_decoding(const string& encoded_text, Node* root) {
    string decoded_output;
    Node* current_node = root;

    for (char bit : encoded_text) {
        if (bit == '0') {
            current_node = current_node->left;
        } else {
            current_node = current_node->right;
        }

        if (current_node->left == nullptr && current_node->right == nullptr) {
            decoded_output += current_node->ch;
            current_node = root;
        }
    }

    return decoded_output;
}

int main() {
    string text;
    cout << "Please enter the text to encode: ";
    getline(cin, text);

    auto [huffman_codes, encoded_text] = huffman_encoding(text);
    cout << "Huffman Codes:" << endl;
    for (const auto& pair : huffman_codes) {
        cout << pair.first << ": " << pair.second << endl;
    }
    cout << "Encoded Text: " << encoded_text << endl;

    string decoded_text = huffman_decoding(encoded_text, build_huffman_tree(text));
    cout << "Decoded Text: " << decoded_text << endl;

    return 0;
}