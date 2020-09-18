package math;

public class Kmp {
	public static void KMPSearch2(String text, String input) 
    { 
    	long start = System.nanoTime();
        int M = input.length(); 
        int N = text.length(); 
  
        // create lps[] that will hold the longest 
        // prefix suffix values for pattern 
        int lps[] = new int[M]; 
        int j = 0; // index for pat[] 
  
        // Preprocess the pattern (calculate lps[] 
        // array) 
        computeLPSArray(input, M, lps); 
  
        int i = 0; // index for txt[] 
        while (i < N) { 
            if (input.charAt(j) == text.charAt(i)) { 
                j++; 
                i++; 
            } 
            if (j == M) { 
                System.out.println("Found pattern "
                                   + "at index " + (i - j)); 
                j = lps[j - 1]; 
            } 
  
            // mismatch after j matches 
            else if (i < N && input.charAt(j) != text.charAt(i)) { 
                // Do not match lps[0..lps[j-1]] characters, 
                // they will match anyway 
    
                if (j != 0 && input.indexOf(text.charAt(i)) != 1) //added comparison on mismatched text char with the list
                    j = lps[j - 1]; 
                else
                    i = i + 1; 
            } 
        } 
        long end = System.nanoTime();
        long elapsedTime = end - start;
        System.out.println("Time Taken for KMP: " + elapsedTime);
    } 
  
  
    public static void computeLPSArray(String input, int M, int lps[]) 
    { 
        // length of the previous longest prefix suffix 
        int len = 0; 
        int i = 1; 
        lps[0] = 0; // lps[0] is always 0 
  
        // the loop calculates lps[i] for i = 1 to M-1 
        while (i < M) { 
            if (input.charAt(i) == input.charAt(len)) { 
                len++; 
                lps[i] = len; 
                i++; 
            } 
            else // (pat[i] != pat[len]) 
            { 
                // This is tricky. Consider the example. 
                // AAACAAAA and i = 7. The idea is similar 
                // to search step. 
                if (len != 0) { 
                    len = lps[len - 1]; 
  
                    // Also, note that we do not increment 
                    // i here 
                } 
                else // if (len == 0) 
                { 
                    lps[i] = len; 
                    i++; 
                } 
            } 
        } 
}
