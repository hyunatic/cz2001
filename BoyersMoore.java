import java.util.Scanner;

public class BoyersMoore {
    public static int[] computeLastOcc(String P) {
        int[] lastOcc = new int[128]; // assume ASCII character set

        for (int i = 0; i < 128; i++) {
            lastOcc[i] = -1; // initialize all elements to -1
        }

        for (int i = 0; i < P.length(); i++) {
            lastOcc[P.charAt(i)] = i; // The LAST value will be store
        }

        return lastOcc;
    }

    public static int BMH(String T, String P) {
        int[] lastOcc;
        int i0, j, m, n;

        n = T.length();
        m = P.length();

        lastOcc = computeLastOcc(P); // Find last occurence of all characters in P

        printLastOcc(lastOcc);

        i0 = 0; // Line P up at T[0]

        while (i0 < (n - m)) {
            j = m - 1; // Start at the last char in P

            System.out.println("+++++++++++++++++++++++++++++++++++++");
            printState(T, P, i0 + j, j);

            while (P.charAt(j) == T.charAt(i0 + j)) {
                j--; // Check "next" (= previous) character

                printState(T, P, i0 + j, j);

                if (j < 0)
                    return (i0); // P found !
            }

            if (j < lastOcc[T.charAt(i0 + j)]) {
                System.out.println("** Bad character caveat detected - slide 1 pos....");
                i0++;
            } else {
                System.out.println("****** lastOcc['" + T.charAt(i0 + j) + "'] = " + lastOcc[T.charAt(i0 + j)]);
                i0 = i0 + j - lastOcc[T.charAt(i0 + j)];
            }
        }

        return -1; // no match
    }

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

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        Scanner in = new Scanner(System.in);

        String T, P;
        int r;

        System.out.println("Try");
        System.out.println("T = abacaxbaccabacbbaabb");
        System.out.println("P = abacbb");
        System.out.println();

        System.out.print("T = ");
        T = in.next();
        System.out.print("P = ");
        P = in.next();

        System.out.println();
        System.out.println(T);
        System.out.println(P);

        r = BMH(T, P);

        System.out.println("Found " + P + " at pos: " + r);
        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        System.out.println(totalTime);
    }

    /*
     * ===================================================== Variables and Methods
     * to make the algorithm visual
     * =====================================================
     */
    public static String T_ruler, P_ruler;

    public static String ruler(int n) {
        String out = "";
        char x = '0';

        for (int i = 0; i < n; i++) {
            out = out + x;
            x++;
            if (x > '9')
                x = '0';
        }

        return out;
    }

    public static void printState(String T, String P, int i, int j) {
        if (T_ruler == null)
            T_ruler = ruler(T.length());

        if (P_ruler == null)
            P_ruler = ruler(P.length());

        System.out.println("=====================================");
        System.out.println("Matching: i = " + i + ", j = " + j);

        System.out.println("   " + T_ruler);
        System.out.println("   " + T);
        System.out.print("   ");
        for (int k = 0; k < i - j; k++)
            System.out.print(" ");
        System.out.println(P);

        System.out.print("   ");
        for (int k = 0; k < i - j; k++)
            System.out.print(" ");
        System.out.println(P_ruler);

        System.out.print("   ");
        for (int k = 0; k < i; k++)
            System.out.print(" ");
        System.out.println("^");

        System.out.print("   ");
        for (int k = 0; k < i; k++)
            System.out.print(" ");
        System.out.println("|");
        System.out.println();
    }

}