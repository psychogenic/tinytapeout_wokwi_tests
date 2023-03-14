## Synchronous/clocked truth table
The lock combination is in "CBA" bits
R is reset, C is clock input bit

Any entry with a bit set to 'c' will:
 * setup any specified bits (0 or 1) and toggle any bits as required
 * then toggle (i.e. invert) the clock bit(s), without changing anything else
 * then re-toggle the same clock bit(s), returning them to their original state
|IN:  CBA  RC  |    output    | comment   |
|--------------|--------------|-----------|
| 000 000  00  | -- ----- -   | init      |
| --- ---  1c  | -- ----- -   | reset     |
| --- ---  0c  | -- ----- -   |           |
| --- 111  -c  | -- 11100 -   |           |
| --- 110  -c  | -- 11111 -   | success   |
| --- 000  tc  | -- ----- -   | reset     |
| --- ---  tc  | -- 11100 -   | locked    |
| --- 111  -c  | -- 11100 -   | bad combo |
| --- 100  -c  | -- 11100 -   | bad combo |
| --- 101  -c  | -- 11100 -   | bad combo |
| --- 100  -c  | -- 11100 -   | bad combo |
| --- 110  -c  | -- 11111 -   | success   |
| --- 000  -c  | -- 11111 -   | still open|
| --- ---  1c  | -- 11100 -   | reset     |
