// engine/tree.cpp
#include <iostream>
#include <algorithm>

struct AVLNode {
    int risk;
    int row, col;
    int height;
    AVLNode* left;
    AVLNode* right;
    AVLNode(int rsk, int r, int c) : risk(rsk), row(r), col(c), height(1), left(nullptr), right(nullptr) {}
};

class AVLTree {
private:
    int height(AVLNode* n) { return n ? n->height : 0; }
    int getBalance(AVLNode* n) { return n ? height(n->left) - height(n->right) : 0; }
    
    AVLNode* rightRotate(AVLNode* y) {
        AVLNode* x = y->left;
        AVLNode* T2 = x->right;
        x->right = y;
        y->left = T2;
        y->height = std::max(height(y->left), height(y->right)) + 1;
        x->height = std::max(height(x->left), height(x->right)) + 1;
        return x;
    }

    AVLNode* leftRotate(AVLNode* x) {
        AVLNode* y = x->right;
        AVLNode* T2 = y->left;
        y->left = x;
        x->right = T2;
        x->height = std::max(height(x->left), height(x->right)) + 1;
        y->height = std::max(height(y->left), height(y->right)) + 1;
        return y;
    }

public:
    AVLNode* root;
    AVLTree() : root(nullptr) {}

    AVLNode* insert(AVLNode* node, int risk, int r, int c) {
        if (!node) return new AVLNode(risk, r, c);
        if (risk < node->risk)
            node->left = insert(node->left, risk, r, c);
        else
            node->right = insert(node->right, risk, r, c);

        node->height = 1 + std::max(height(node->left), height(node->right));
        int balance = getBalance(node);

        if (balance > 1 && risk < node->left->risk) return rightRotate(node);
        if (balance < -1 && risk > node->right->risk) return leftRotate(node);
        if (balance > 1 && risk > node->left->risk) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        if (balance < -1 && risk < node->right->risk) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        return node;
    }
};