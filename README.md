<h1># NotSoRandom</h1>
<h3>A python script and class that exploits the deterministic nature of java.util.Random() for two simple cases.</h3>
<p>
The script/class is based on java.util.Random algorithms and values. For other packages you would have to adjust the MULT / ADD / MASK values manually. Depending on the algorithms used additional manual changes would be necessary.
</p>
<p>
  <strong>Case 1</strong>: a long (64bit) rnd number is known. NotSoRandom() allows to calculate the seed and either previous and next long rnd values based on the found seed.</br>
  <strong>Case 2</strong>: two sequentially calculated rnd int numbers are known. NotSoRandom() allows to calculate the seed and either previous and next int rnd values based on the found seed.</br>
</p>
<p>
An example script 'get_previous_long.py' is provided that illustrates the usage of class NotSoRandom.
</p>
