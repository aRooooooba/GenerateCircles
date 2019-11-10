# Draw Circles

## Demands

Start with a single window containing a grid of $20\times20$ points.

All points start out grey.

Have a button at the bottom of the window called "Generate".

The user can toggle points on and off.

Generate a circle and a ellipses that best fits the highlighted points.



## Environment

Ubuntu 18.04.3 LTS, Vim, Python 3.6.8, wxPython 4, sympy 1.5.dev0



## Structure

**class MyFrame(wx.Frame)**

Methods

---

- \_\_init\_\_(*self, \*args, \*\*kw*)

  \_\_init\_\_(*self*)

  \_\_init\_\_(*self, parent, id=ID_ANY, title='', pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr*)

  Constructor, creating the window, including the $20\times20$ points, panel and the generate button. It is also responsible for binding events.

- onLeftUp(*self, event*)

  Invoke when the left mouse button changes to up.

  If the generate button is just pressed, we should clear all the graphs and reinitialize the grid. If not, then we go on turning on or off the points.

- onGenerate(*self, event*)

  Invoke when the generate button is clicked.

  We can only determin an optimal circle with more than or equal to 3 points. So if not point is chosen, no circle will be generated. If only choose one point, a fixed small circle will occur, and if only choose two points, a smallest circle across the points will occur.

  If more points are chosen, we use the least squares method to get the optimal circle.
  
We are looking for the center (A, B) and the radius R, and try to make $R^2=(x-A)^2+(y-B)^2$. So we get $x^2-2Ax+A^2+y^2-2By+B^2-R^2=0$.
  
Let $a=-2A$, $b=-2B$, $c=A^2+B^2-R^2$, we can get a simplified formula $x^2+y^2+ax+by+c=0$. For all the points, we need to make $S=\sum(x_i^2+y_i^2+ax_i+by_i+c)^2$ as small as possible to fit the points. So we du calculus and set $\frac{\partial Q}{\partial a}=\frac{\partial Q}{\partial b}=\frac{\partial Q}{\partial c}=0$ to get the minimum value.
  
  In some cases, for example the points form a straight line, c will not be solvable. Then a random point is created and make the whole formula solvable.
  
  

Properties

---

- buttonPool: stores all the $20\times20$ points
- onPoints: stores the points which are turned on
- isShowing: binary, True when it's showing circles, False otherwise



## Result

![Screenshot from 2019-11-09 22-49-51](/home/xingjian/Pictures/Screenshot from 2019-11-09 22-49-51.png)

![Screenshot from 2019-11-09 22-50-09](/home/xingjian/Pictures/Screenshot from 2019-11-09 22-50-09.png)

![Screenshot from 2019-11-09 22-50-30](/home/xingjian/Pictures/Screenshot from 2019-11-09 22-50-30.png)

![Screenshot from 2019-11-09 22-51-56](/home/xingjian/Pictures/Screenshot from 2019-11-09 22-51-56.png)

![Screenshot from 2019-11-09 22-52-26](/home/xingjian/Pictures/Screenshot from 2019-11-09 22-52-26.png)



## To be improved

As for the ellipse, I can not understand the formula in papers, and it seems that wxPython cannot draw a casual ellipse. So when I have more than two points, I will generate a very easy ellipse, which is far from satisfactory.