Animal
======
This is how fitness is calculated:

.. math::

 \Phi =
 \begin{cases}
 0  &\text{if $weight\leq0$} \\
 \frac{1}{1 + e^{\phi_{age}*(age -a_{half})}} \times \frac{1}{1 + e^{-\phi_{weight}*(weight -w_{half})}}
 \end{cases}

This is how the probability of birth is calculated where N is the number of animal in the cell:

.. math::

 P _{birth} =
 \begin{cases}
 0  &\text{if $weight<\zeta(w _{birth} + \sigma_{birth})$} \\
 min(1, \gamma \times \Phi \times (N-1) )
 \end{cases}

This is how the probability of death is calculated:

 P _{death} =
 \begin{cases}
 0  &\text{if $weight\leq0$} \\
 \omega(1-\Phi)
 \end{cases}

.. automodule:: biosim.animal
    :members: