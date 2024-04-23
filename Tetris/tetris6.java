package Tetris;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;

public class tetris6 extends JPanel {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Tetris");
        tetris6 tetris = new tetris6();
        frame.add(tetris);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
        tetris.start();
    }

    private final int BOARD_WIDTH = 10;
    private final int BOARD_HEIGHT = 22;
    private final int DELAY = 300;

    private Timer timer;
    private boolean isFallingFinished = false;
    private boolean isStarted = false;
    private boolean isPaused = false;
    private int numLinesRemoved = 0;
    private int curX = 0;
    private int curY = 0;
    private Shape curPiece;
    private Shape.Tetrominoes[] board;
    private Color[] colors = {new Color(0, 0, 0), new Color(204, 102, 102),
            new Color(102, 204, 102), new Color(102, 102, 204),
            new Color(204, 204, 102), new Color(204, 102, 204),
            new Color(102, 204, 204), new Color(218, 170, 0)
    };

    public tetris6() {
        initBoard();
    }

    private void initBoard() {
        setFocusable(true);
        addKeyListener(new TAdapter());
        setBackground(Color.BLACK);
        setPreferredSize(new Dimension(200, 400));

        board = new Shape.Tetrominoes[BOARD_WIDTH * BOARD_HEIGHT];
        clearBoard();

        timer = new Timer(DELAY, new GameCycle());
    }

    private void clearBoard() {
        for (int i = 0; i < BOARD_HEIGHT * BOARD_WIDTH; i++) {
            board[i] = Shape.Tetrominoes.NoShape;
        }
    }

    private void drawSquare(Graphics g, int x, int y, Shape.Tetrominoes shape) {
        Color color = colors[shape.ordinal()];

        g.setColor(color);
        g.fillRect(x + 1, y + 1, squareWidth() - 2, squareHeight() - 2);
        g.setColor(color.brighter());
        g.drawLine(x, y + squareHeight() - 1, x, y);
        g.drawLine(x, y, x + squareWidth() - 1, y);
        g.setColor(color.darker());
        g.drawLine(x + 1, y + squareHeight() - 1,
                x + squareWidth() - 1, y + squareHeight() - 1);
        g.drawLine(x + squareWidth() - 1, y + squareHeight() - 1,
                x + squareWidth() - 1, y + 1);
    }

    private void doDrawing(Graphics g) {
        Dimension size = getSize();
        int boardTop = (int) size.getHeight() - BOARD_HEIGHT * squareHeight();

        for (int i = 0; i < BOARD_HEIGHT; i++) {
            for (int j = 0; j < BOARD_WIDTH; j++) {
                Shape.Tetrominoes shape = shapeAt(j, BOARD_HEIGHT - i - 1);
                if (shape != Shape.Tetrominoes.NoShape) {
                    drawSquare(g, j * squareWidth(),
                            boardTop + i * squareHeight(), shape);
                }
            }
        }
    
        if (curPiece.getShape() != Shape.Tetrominoes.NoShape) {
            for (int i = 0; i < 4; i++) {
                int x = curX + curPiece.x(i);
                int y = curY - curPiece.y(i);
                drawSquare(g, x * squareWidth(),
                        boardTop + (BOARD_HEIGHT - y - 1) * squareHeight(),
                        curPiece.getShape());
            }
        }
        
        if (!isStarted) {
            showStartMessage(g);
        } else if (isPaused) {
            showPauseMessage(g);
        } else if (!isFallingFinished) {
            showGameOverMessage(g);
        }
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        doDrawing(g);
    }

    private int squareWidth() {
        return (int) getSize().getWidth() / BOARD_WIDTH;
    }

    private int squareHeight() {
        return (int) getSize().getHeight() / BOARD_HEIGHT;
    }

    private Shape.Tetrominoes shapeAt(int x, int y) {
        return board[y * BOARD_WIDTH + x];
    }

    private void start() {
        isStarted = true;
        isFallingFinished = false;
        numLinesRemoved = 0;
        clearBoard();

        newPiece();
        timer.start();
    }

    private void pause() {
        if (!isStarted) {
            return;
        }

        isPaused = !isPaused;
        if (isPaused) {
            timer.stop();
        } else {
            timer.start();
        }

        repaint();
    }

    public void gameOver() {
        timer.stop();
        isStarted = false;
    }

    private void removeFullLines() {
        int numFullLines = 0;
        for (int i = BOARD_HEIGHT - 1; i >= 0; i--) {
            boolean lineIsFull = true;
            for (int j = 0; j < BOARD_WIDTH; j++) {
                if (shapeAt(j, i) == Shape.Tetrominoes.NoShape) {
                    lineIsFull = false;
                    break;
                }
            }
            if (lineIsFull) {
                numFullLines++;
                for (int k = i; k < BOARD_HEIGHT - 1; k++) {
                    for (int j = 0; j < BOARD_WIDTH; j++) {
                        board[k * BOARD_WIDTH + j] = shapeAt(j, k + 1);
                    }
                }
            }
        }

        if (numFullLines > 0) {
            numLinesRemoved += numFullLines;
            repaint();
        }
    }

    private void newPiece() {
        curPiece = new Shape();
        curPiece.setRandomShape();
        curX = BOARD_WIDTH / 2 + 1;
        curY = BOARD_HEIGHT - 1 + curPiece.minY();

        if (!tryMove(curPiece, curX, curY)) {
            curPiece.setShape(Shape.Tetrominoes.NoShape);
            timer.stop();
            isStarted = false;
        }
    }

    public int minY() {
        int[][] coordinates = new int[4][2]; // Initialize the coordinates variable
        int minY = coordinates[0][1];
        for (int i = 1; i < 4; i++) {
            minY = Math.min(minY, coordinates[i][1]);
        }
        return minY;
    }

    private boolean tryMove(Shape newPiece, int newX, int newY) {
        for (int i = 0; i < 4; i++) {
            int x = newX + newPiece.x(i);
            int y = newY - newPiece.y(i);
            if (x < 0 || x >= BOARD_WIDTH || y < 0 || y >= BOARD_HEIGHT) {
                return false;
            }
            if (shapeAt(x, y) != Shape.Tetrominoes.NoShape) {
                return false;
            }
        }

        curPiece = newPiece;
        curX = newX;
        curY = newY;
        repaint();

        return true;
    }

    private void dropDown() {
        int newY = curY;
        while (newY > 0) {
            if (!tryMove(curPiece, curX, newY - 1)) {
                break;
            }
            newY--;
        }
        pieceDropped();
    }

    private void oneLineDown() {
        if (!tryMove(curPiece, curX, curY - 1)) {
            pieceDropped();
        }
    }

    private void pieceDropped() {
        for (int i = 0; i < 4; i++) {
            int x = curX + curPiece.x(i);
            int y = curY - curPiece.y(i);
            board[y * BOARD_WIDTH + x] = curPiece.getShape();
        }

        removeFullLines();

        if (!isFallingFinished) {
            newPiece();
        }
    }

    private void rotate() {
        Shape newPiece = curPiece.rotateRight();
        if (tryMove(newPiece, curX, curY)) {
            curPiece = newPiece;
        }
    }
    public class Shape {

        public enum Tetrominoes { NoShape, ZShape, SShape, LineShape, TShape, SquareShape, LShape, MirroredLShape }
    
        private Tetrominoes pieceShape;
        private int[][] coordinates;
    
        public Shape() {
            coordinates = new int[4][2];
            setShape(Tetrominoes.NoShape);
        }
    
        public int minY() {
            // TODO Auto-generated method stub
            throw new UnsupportedOperationException("Unimplemented method 'minY'");
        }

        public void setShape(Tetrominoes shape) {
            pieceShape = shape;
            switch (shape) {
                case NoShape:
                    coordinates = new int[][]{{0, 0}, {0, 0}, {0, 0}, {0, 0}};
                    break;
                case ZShape:
                    coordinates = new int[][]{{0, -1}, {0, 0}, {-1, 0}, {-1, 1}};
                    break;
                case SShape:
                    coordinates = new int[][]{{0, -1}, {0, 0}, {1, 0}, {1, 1}};
                    break;
                case LineShape:
                    coordinates = new int[][]{{0, -1}, {0, 0}, {0, 1}, {0, 2}};
                    break;
                case TShape:
                    coordinates = new int[][]{{-1, 0}, {0, 0}, {1, 0}, {0, 1}};
                    break;
                case SquareShape:
                    coordinates = new int[][]{{0, 0}, {1, 0}, {0, 1}, {1, 1}};
                    break;
                case LShape:
                    coordinates = new int[][]{{-1, -1}, {0, -1}, {0, 0}, {0, 1}};
                    break;
                case MirroredLShape:
                    coordinates = new int[][]{{1, -1}, {0, -1}, {0, 0}, {0, 1}};
                    break;
            }
        }

        public void setRandomShape() {
            Tetrominoes[] values = Tetrominoes.values();
            int randomIndex = (int) (Math.random() * values.length);
            setShape(values[randomIndex]);
        }
    
        public int x(int index) {
            return coordinates[index][0];
        }
    
        public int y(int index) {
            return coordinates[index][1];
        }
    
        public Tetrominoes getShape() {
            return pieceShape;
        }
    
        public Shape rotateRight() {
            // Implement rotation logic
            // ...
    
            return this;
        }
    }
    class TAdapter extends KeyAdapter {

        @Override
        public void keyPressed(KeyEvent e) {
            if (!isStarted || curPiece.getShape() == Shape.Tetrominoes.NoShape) {
                return;
            }

            int keycode = e.getKeyCode();

            if (keycode == 'p' || keycode == 'P') {
                pause();
                return;
            }

            if (isPaused) {
                return;
            }

            switch (keycode) {
                case KeyEvent.VK_LEFT:
                    tryMove(curPiece, curX - 1, curY);
                    break;
                case KeyEvent.VK_RIGHT:
                    tryMove(curPiece, curX + 1, curY);
                    break;
                case KeyEvent.VK_DOWN:
                    oneLineDown();
                    break;
                case KeyEvent.VK_UP:
                    rotate();
                    break;
                case KeyEvent.VK_SPACE:
                    dropDown();
                    break;
            }
        }
    }

    class GameCycle implements ActionListener {

        @Override
        public void actionPerformed(ActionEvent e) {
            doGameCycle();
        }
    }

    private void doGameCycle() {
        update();
        repaint();
    }

    private void update() {
        if (isPaused) {
            return;
        }

        if (isFallingFinished) {
            isFallingFinished = false;
            newPiece();
        } else {
            oneLineDown();
        }
    }

    private void showStartMessage(Graphics g) {
        String msg = "Press Enter to Start";
        Font small = new Font("Helvetica", Font.BOLD, 14);
        FontMetrics fm = getFontMetrics(small);

        g.setColor(Color.white);
        g.setFont(small);
        g.drawString(msg, (BOARD_WIDTH * squareWidth() - fm.stringWidth(msg)) / 2,
                BOARD_HEIGHT * squareHeight() / 2);
    }

    private void showPauseMessage(Graphics g) {
        String msg = "Paused";
        Font small = new Font("Helvetica", Font.BOLD, 14);
        FontMetrics fm = getFontMetrics(small);

        g.setColor(Color.white);
        g.setFont(small);
        g.drawString(msg, (BOARD_WIDTH * squareWidth() - fm.stringWidth(msg)) / 2,
                BOARD_HEIGHT * squareHeight() / 2);
    }

    private void showGameOverMessage(Graphics g) {
        String msg = "Game Over";
        Font small = new Font("Helvetica", Font.BOLD, 14);
        FontMetrics fm = getFontMetrics(small);

        g.setColor(Color.white);
        g.setFont(small);
        g.drawString(msg, (BOARD_WIDTH * squareWidth() - fm.stringWidth(msg)) / 2,
                BOARD_HEIGHT * squareHeight() / 2);
    }
}
