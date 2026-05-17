// engine/main.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include "linked_list.cpp"
#include "tree.cpp"

using namespace std;

struct District {
    int row, col, risk;
    string state; // "healthy", "infected", "vaccinated", "quarantined"
};

District grid[8][8];
int currentTurn = 1;
LinkedList infectionChain;
AVLTree riskTree;

void initGrid() {
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            grid[r][c].row = r;
            grid[r][c].col = c;
            grid[r][c].risk = (rand() % 10) + 1;
            grid[r][c].state = "healthy";
            riskTree.root = riskTree.insert(riskTree.root, grid[r][c].risk, r, c);
        }
    }
    int ir = rand() % 8;
    int ic = rand() % 8;
    grid[ir][ic].state = "infected";
    infectionChain.insert(ir, ic, currentTurn);
}

void saveState() {
    ofstream file("data/state.json");
    file << "{\n  \"turn\": " << currentTurn << ",\n  \"grid\": [\n";
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            file << "    {\"row\": " << r << ", \"col\": " << c 
                 << ", \"risk\": " << grid[r][c].risk 
                 << ", \"state\": \"" << grid[r][c].state << "\"}";
            if (r == 7 && c == 7) file << "\n"; else file << ",\n";
        }
    }
    file << "  ],\n  \"infection_chain\": [\n";
    ListNode* curr = infectionChain.head;
    while (curr) {
        file << "    {\"row\": " << curr->row << ", \"col\": " << curr->col << ", \"turn\": " << curr->turn << "}";
        if (curr->next) file << ",\n"; else file << "\n";
        curr = curr->next;
    }
    file << "  ]\n}";
    file.close();
}

void loadActionAndProcess() {
    ifstream file("data/action.json");
    if (!file.is_open()) return;
    
    string line;
    int targetRow = -1, targetCol = -1;
    string actionType = "";
    
    while (getline(file, line)) {
        if (line.find("action_type") != string::npos) {
            if (line.find("vaccinate") != string::npos) actionType = "vaccinate";
            if (line.find("skip") != string::npos) actionType = "skip";
        }
        if (line.find("row") != string::npos) {
            stringstream ss(line); string dummy; int val;
            while(ss >> dummy) { if (stringstream(dummy) >> val) targetRow = val; }
        }
        if (line.find("col") != string::npos) {
            stringstream ss(line); string dummy; int val;
            while(ss >> dummy) { if (stringstream(dummy) >> val) targetCol = val; }
        }
    }
    file.close();
    remove("data/action.json");

    if (actionType == "vaccinate" && targetRow != -1 && targetCol != -1) {
        if (grid[targetRow][targetCol].state == "healthy") {
            grid[targetRow][targetCol].state = "vaccinated";
        }
    }

    // Spread logic (4-connectivity)
    bool nextInfected[8][8] = {false};
    int dr[] = {-1, 1, 0, 0};
    int dc[] = {0, 0, -1, 1};

    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            if (grid[r][c].state == "infected") {
                for (int i = 0; i < 4; i++) {
                    int nr = r + dr[i];
                    int nc = c + dc[i];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        if (grid[nr][nc].state == "healthy") {
                            if ((rand() % 10) < grid[nr][nc].risk) {
                                nextInfected[nr][nc] = true;
                            }
                        }
                    }
                }
            }
        }
    }

    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            if (nextInfected[r][c]) {
                grid[r][c].state = "infected";
                infectionChain.insert(r, c, currentTurn + 1);
            }
        }
    }
    currentTurn++;
    saveState();
}

int main() {
    srand(time(0));
    ifstream check("data/state.json");
    if (!check.is_open()) {
        initGrid();
        saveState();
    } else {
        check.close();
        // Cargar estado anterior simulado para mantener persistencia simplificada
        // Para este entregable inicial, reinicializa o procesa acción directa
        loadActionAndProcess();
    }
    return 0;
}