# alibaba
Zero knowledge authentication using the Feige-Fiat-Shamir identification scheme built into an interactive application using Tkinter. The original paper can be found at https://link.springer.com/article/10.1007/BF02351717. 

## Zero-Knowledge proofs
Consider two parties, Peggy (Prover) and Victor (Verifier). Peggy wishes to authenticate herself with Victor, however she does not wish to share her password. A Zero-Knowledge proof is a method to allow Peggy to prove that she knows her password, without actually having to reveal her password. This is accomplished by having Victor ask Peggy a set of questions, which she can answer correctly only if she knows her password.

## Feige-Fiat-Shamir
Developed by Uriel Feige, Amos Fiat, and Adi Shamir in 1988, FFS is an example of a Zero-Knowledge Proof which works on modular arithmetic and relies on the security of the Prime Factorization problem. The procedure is as follows:

##### Registration
1. Peggy chooses two large (in our case, 50 bit) primes p and q and computes *N = pq* <br>
2. Peggy then creates her secret numbers w<sub>1</sub>, ... , w<sub>k</sub> coprime to N<br>
3. Peggy calculates _v<sub>i</sub><sup>2</sup> ≡ w<sub>i</sub><sup>2</sup> (mod N)_<br>
4. Peggy finally sends Victor N and v<sub>1</sub>, ... , v<sub>k</sub> <br>
5. Peggy saves her secret credentials, __{N, [w<sub>1</sub>, ... , w<sub>k</sub>] }__ along with her username of choice<br>
6. Victor stores Peggy's record as __{N, [v<sub>1</sub>, ... , v<sub>k</sub>]}__ against Peggy's username <br>

##### Authentication
1. Peggy chooses random integers x<sub>1</sub>, ... , x<sub>k</sub> coprime to N and computes _y ≡ x<sub>i</sub> w<sub>i</sub><sup>2</sup> (mod N)_. Peggy then sends _y_ to Victor <br>
2. Victor creates a string of random bits b<sub>i</sub> of length k. Victor sends these numbers to Peggy.
3. Peggy computes _z ≡ y*w<sub>i</sub><sup>b<sub>i</sub></sup> (mod N)_. Peggy then sends _z_ to Victor.<br>
4. Victor verifies that _z<sup>2</sup> ≡ y * v<sup>b<sub>i</sub></sup> (mod N)_ <br>
This procedure, called a trial is repeated as many times as required with different values of x and b<sub>i</sub> until Victor is satisfied that he is indeed talking to Peggy.
<br>
Note: In the original paper, only one random number r is used, which is multiplied with the every secret number. Our implementation uses k random numbers, each multiplied with their respective secret number.

## Security
The security of the protocol follows from the zero-knowledge proof. Peggy never reveals her secret numbers, only the square of the numbers modulo N, and N. If an eavesdropper Eve were to be listening in, she would learn Victor's _v<sub>i</sub>_, but since she does not know Peggy's secret numbers, she would not be able to pose as Peggy. If she had to convice Victor that she was Peggy, she would have to correctly guess what Victors _b<sub>i</sub>_ will be, and calculate her _x_ accordingly and send it. <br>
<br>
The probability that Eve coorectly guesses this for _k_ secret numbers in _t_ trials is __2<sup>-kt</sup>__. Our implementation uses 5 secret numbers and runs 10 trials; the probability of successfullly posing as Peggy is thus, one in __2<sup>50</sup>__

