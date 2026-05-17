// engine/linked_list.cpp
#include <iostream>

struct ListNode {
    int row, col, turn;
    ListNode* next;
    ListNode(int r, int c, int t) : row(r), col(c), turn(t), next(nullptr) {}
};

class LinkedList {
public:
    ListNode* head;
    ListNode* tail;
    
    LinkedList() : head(nullptr), tail(nullptr) {}
    
    void insert(int r, int c, int t) {
        ListNode* newNode = new ListNode(r, c, t);
        if (!head) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
    }
    
    ~LinkedList() {
        ListNode* current = head;
        while (current != nullptr) {
            ListNode* nextNode = current->next;
            delete current;
            current = nextNode;
        }
    }
};