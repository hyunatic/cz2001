import java.io.*;
import java.util.Scanner;

public class SearchAlgo {
    interface CreateIntReturnFunction {
        public int Run(int a, int b);
    }

    interface CreateVoidReturnFunction {
        public void Run(String a, int b, int c[]);
    }

    public static void main(String args[]) throws IOException {
        String file = ReadFile();
        Scanner sc = new Scanner(System.in);
        int choice = 0;
        System.out.println("Enter Substring comparision: ");
        String input = sc.nextLine();

        System.out.println("Select Search Algorithm: ");
        System.out.println("1: Brute Force");
        System.out.println("2: Boyers Moore");
        System.out.println("3: KMP");

        choice = sc.nextInt();
        switch (choice) {
            case 1:
                BruteForce(file, input);
                main(args);
            case 2:
                BoyersMoore(file, input);
                main(args);
            case 3:
                KMP(file, input);
                main(args);

            default:
                sc.close();
                System.exit(0);
        }
    };

    // -------------- Reading external text file ---------//
    public static String ReadFile() throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader("Template.txt"));
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

    // ------------------------------------ Brute Force
    // ----------------------------------------------------------//
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
    // ---------------------------------------------- Boyers Moore
    // -------------------------------------------------//
    public static void BoyersMoore(String file, String pattern) {
        // Create a function to shift pattern to the right when character is mismatched
        // (Java 8 Style)
        // shifting of the pattern to the "right" of the text
        CreateVoidReturnFunction charShifter = (str, size, badchar) -> {
            int i;

            char[] strArray = str.toCharArray();
            // reset placement of all to -1 index
            for (i = 0; i < 256; i++)
                badchar[i] = -1;
            // set pattern position
            for (i = 0; i < size; i++)
                badchar[(int) strArray[i]] = i;
        };
        // Create a function find the Bigger number between 2 numbers (Java 8 Style)
        CreateIntReturnFunction FindMaxNum = (x, y) -> (x > y) ? x : y;

        long start = System.nanoTime();
        int patternlength = pattern.length();
        int filelength = file.length();

        int badchar[] = new int[256];
        charShifter.Run(pattern, patternlength, badchar);
        int length_index = 0;

        while (length_index <= (filelength - patternlength)) {
            int pattern_index = patternlength - 1;
            while (pattern_index >= 0 && pattern.charAt(pattern_index) == file.charAt(length_index + pattern_index) && pattern.charAt(0) == file.charAt(length_index)) 
                pattern_index--;
                // --- Match ---//
            if (pattern_index < 0) {
                System.out.println("Patterns occur at index = " + length_index);
                length_index += (length_index + patternlength < filelength)
                        ? patternlength - badchar[file.charAt(length_index + patternlength)]
                        : 1;
            } else
                length_index += FindMaxNum.Run(1, pattern_index - badchar[file.charAt(length_index + pattern_index)]);
                // --- Mismatch ---//
                // Return Num of pattern found in file
               
        }
        long end = System.nanoTime();
        long elapsedTime = end - start;
        System.out.println("Time Taken for Boyers Moore: " + elapsedTime);
    }
    // --------------------------------------- KMP --------------------------------------------------

    public static void KMP(String file, String pattern) {
        //Create function to Find Sub Patterns in the text
        //Calculate the lps array
        CreateVoidReturnFunction FindPrepocessingPattern = (pat, patternlength, lpsarr) -> {
            // length of the previous longest prefix suffix
            int length = 0;
            int i = 1;
            lpsarr[0] = 0; // lps[0] is always 0
            // the loop calculates lps[i] for i = 1 to M-1
            while (i < patternlength) {
                if (pat.charAt(i) == pat.charAt(length)) {
                    length++;
                    lpsarr[i] = length;
                    i++;
                } else{
                    // Consider the example.
                    // AAACAAAA and i = 7. The idea is similar
                    // to search step.
                    if (length != 0) {
                        length = lpsarr[length - 1];
                    } else{
                        lpsarr[i] = length;
                        i++;
                    }
                }
            }
        };
        long start = System.nanoTime();
        int M = pattern.length();
        int N = file.length();

        // create lps[] that will hold the longest
        // prefix suffix values for pattern
        int lps[] = new int[M];
        int pattern_index = 0; // index for pat[]

        // Preprocess the pattern (calculate lps[] array)
        FindPrepocessingPattern.Run(pattern, M, lps);

        int text_index = 0; // index for txt[]
        while (text_index < N) {
            if (pattern.charAt(pattern_index) == file.charAt(text_index)) {
                pattern_index++;
                text_index++;
            }
            if (pattern_index == M) {
                System.out.println("Found pattern " + "at index " + (text_index - pattern_index));
                pattern_index = lps[pattern_index - 1];
            }
            // mismatch after j matches
            else if (text_index < N && pattern.charAt(pattern_index) != file.charAt(text_index)) {
                //Make comparison on mismatched text char with the list
                if (pattern_index != 0 && pattern.indexOf(file.charAt(text_index)) != 1) 
                    pattern_index = lps[pattern_index - 1];
                else
                    text_index = text_index + 1;
            }
        }
        long end = System.nanoTime();
        long elapsedTime = end - start;
        System.out.println("Time Taken for KMP: " + elapsedTime);
    }

}
