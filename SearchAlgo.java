import java.io.*;
import java.util.Scanner;

public class SearchAlgo {
    public static void main(String args[]) throws IOException {
        String file = ReadFile();
        Scanner sc = new Scanner(System.in);
        int choice = 0;
        System.out.println("Enter Substring comparision: ");
        String input = sc.nextLine();

        System.out.println("Select Search Algorithm: ");
        System.out.println("1: Brute Force");
        System.out.println("2: Boyers Moore");
        System.out.println("3: BNDM");

        choice = sc.nextInt();
        switch (choice) {
            case 1:
                BruteForce(file, input);
                main(args);
            case 2:
                BoyersMoore(file, input);
                main(args);
            case 3:
                BNDM(file, input);
                main(args);
            default:
                sc.close();
                System.exit(0);
        }  
    };
// -------------- Reading external text file ---------//
    public static String ReadFile() throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader("Testing.txt"));
        StringBuilder stringBuilder = new StringBuilder();
        try {
            while (reader.readLine() != null) {
                stringBuilder.append(reader.readLine());
            }
            reader.close();
            // Remove the null characters
            stringBuilder.setLength(stringBuilder.length() - 4);
        } catch (FileNotFoundException e) {
            e.getMessage();
        } finally {
            return stringBuilder.toString();
        }
    }
//------------------------------------ Brute Force ----------------------------------------------------------//
    public static void BruteForce(String text, String input) {
        long start = System.nanoTime();

        System.out.println("Searching Pattern: " + input);
        for (int i = 0; i < text.length() - input.length(); i++) {
            String charIterator = text.substring(i, i + input.length());
            if (input.equals(charIterator))
                System.out.println("Pattern Found in index: " + i);
        }

        long end = System.nanoTime();
        long elapsedTime = end - start;
        System.out.println("Time Taken for Brute Force: " + elapsedTime);
    }
//---------------------------------------------- Boyers Moore -------------------------------------------------//

    static int max(int a, int b) { // Return Num of pattern found in file
        return (a > b) ? a : b;
    }
// shifting of the pattern to the "right" of the text
    static void badCharHeuristic(char[] str, int size, int badchar[]) {
        int i;
        //reset placement of all to -1 index
        for (i = 0; i < 256; i++)
            badchar[i] = -1;
        //set pattern position
        for (i = 0; i < size; i++)
            badchar[(int) str[i]] = i;
    }

    public static void BoyersMoore(String file, String pattern) {
        long start = System.nanoTime();
        int patternlength = pattern.length();
        int filelength = file.length();

        int badchar[] = new int[256];
        badCharHeuristic(pattern.toCharArray(), patternlength, badchar);
        int length_index = 0;

        while (length_index <= (filelength - patternlength)) {
            int pattern_index = patternlength - 1;
            while (pattern_index >= 0 && pattern.charAt(pattern_index) == file.charAt(length_index + pattern_index) && pattern.charAt(0) == file.charAt(length_index)) //--- Match ---//
                pattern_index--;
            if (pattern_index < 0) { //--- Mismatch ---//
                System.out.println("Patterns occur at index = " + length_index);
                length_index += (length_index + patternlength < filelength) ? patternlength - badchar[file.charAt(length_index + patternlength)] : 1;

            } else
                length_index += max(1, pattern_index - badchar[file.charAt(length_index + pattern_index)]);
        }
        long end = System.nanoTime();
        long elapsedTime = end - start;
        System.out.println("Time Taken for Boyers Moore: " + elapsedTime);
    }
//------------------------------------------------------- BNDM ------------------------------------------------------
    public static void printLastOcc(int[] lastOcc) {
        int i, j = 0;

        System.out.println();
        for (i = (int) 'a'; i <= (int) 'z'; i++) {
            System.out.print((char) i + " " + lastOcc[i] + "; ");
            if (++j % 13 == 0)
                System.out.println();
        }
        System.out.println();
        System.out.println();
    }

    public static void BNDM(String file, String pattern) {
        long start = System.nanoTime();
        if (pattern.length() == file.length() && pattern.equals(file)) {
            System.out.println("Sequence = Source");
        }

        char[] x = pattern.toCharArray(), y = pattern.toCharArray();
        int i, j, s, d, last, m = x.length, n = y.length;
        int[] b = new int[256];
        //----- initalize empty list with 0
        for (i = 0; i < b.length; i++) {
            b[i] = 0;
        }
        s = 1;
        //-------- Set pattern index within main file/text -----------
        for (i = m - 1; i >= 0; i--) {
            b[x[i]] |= s;
            s <<= 1;
        }

        j = 0;
        while (j <= n - m) {
            i = m - 1;
            last = m;
            d = ~0;
            while (i >= 0 && d != 0) {
                d &= b[y[j + i]];
                i--;
                if (d != 0) {
                    if (i >= 0) {
                        last = i + 1;
                    } else {
                        System.out.println("Pattern found in starting from index: " + j);
                    }
                }
                d <<= 1;
            }
            j += last;
        }
        long end = System.nanoTime();
        long elapsedTime = end - start;
        System.out.println("Time Taken for BNDM: " + elapsedTime);
    }

}
