package ristinolla;
import java.util.Scanner;

public class TicTacToe2 {
    private char[][] board;
    private char currentPlayer;
    
    public TicTacToe2() {
        board = new char[3][3];
        currentPlayer = 'X';
        initializeBoard();
    }
    
    private void initializeBoard() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[i][j] = '-';
            }
        }
    }
    
    private void printBoard() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    private boolean isBoardFull() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == '-') {
                    return false;
                }
            }
        }
        return true;
    }
    
    private boolean isGameOver() {
        return checkRows() || checkColumns() || checkDiagonals();
    }
    
    private boolean checkRows() {
        for (int i = 0; i < 3; i++) {
            if (board[i][0] != '-' && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
                return true;
            }
        }
        return false;
    }
    
    private boolean checkColumns() {
        for (int i = 0; i < 3; i++) {
            if (board[0][i] != '-' && board[0][i] == board[1][i] && board[1][i] == board[2][i]) {
                return true;
            }
        }
        return false;
    }
    
    private boolean checkDiagonals() {
        if (board[0][0] != '-' && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
            return true;
        }
        if (board[0][2] != '-' && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
            return true;
        }
        return false;
    }
    
    private void makeMove(int row, int col) {
        if (row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == '-') {
            board[row][col] = currentPlayer;
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
        }
    }
    
    public void play() {
        Scanner scanner = new Scanner(System.in);
        
        while (!isGameOver() && !isBoardFull()) {
            System.out.println("Current board:");
            printBoard();
            
            System.out.println("Player " + currentPlayer + ", enter your move (row and column):");
            int row = -1;
            int col = -1;
            
            while (row < 0 || row >= 3 || col < 0 || col >= 3 || board[row][col] != '-') {
                System.out.print("Enter row (0-2): ");
                try {
                    row = scanner.nextInt();
                } catch (Exception e) {
                    System.out.println("Invalid input. Try again.");
                    scanner.nextLine(); // Clear the input buffer
                    continue;
                }
                
                System.out.print("Enter column (0-2): ");
                try {
                    col = scanner.nextInt();
                } catch (Exception e) {
                    System.out.println("Invalid input. Try again.");
                    scanner.nextLine(); // Clear the input buffer
                }
                
                if (row < 0 || row >= 3 || col < 0 || col >= 3 || board[row][col] != '-') {
                    System.out.println("Invalid move. Try again.");
                }
            }
            
            makeMove(row, col);
        }
        
        System.out.println("Final board:");
        printBoard();
        
        if (isGameOver()) {
            System.out.println("Player " + currentPlayer + " wins!");
        } else {
            System.out.println("It's a draw!");
        }
        
        scanner.close();
    }
    
    public static void main(String[] args) {
        TicTacToe2 game = new TicTacToe2();
        game.play();
    }
}