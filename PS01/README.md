# Problem set 01 - Computer Vision

### By: Daniel Santana Santos - *201712040057* - Feb/2021

Python language was used to complete this problem set. Due to the vast number of libraries that Python has available,
a few of these were used to speed up the process of calculating means, DFT's, plotting graphs etc. Specifically for this
PS, Numpy and Matplotlib libraries were used. To run the code, please run `pip install -r requirements.txt` on the
command line beforehand, at the project root directory. Then, on `main.py`, specify which formulation you would like to
execute, and which sub-problem of if. Each formulation is a class, with the name of "FormulationX", where X is the 
number of the formulation, and each sub-problem simply has the name of its number. To run the code after you have 
specified all of these, simply run `python main.py` while inside the `PS01` directory.

### Formulation 01
Formulation 01 consists in four sub-problems meaning to train the student into managing images and extracting
information from them using OpenCV. For this, the student was asked to show an RGB image on the screen, its histogram,
and lastly, a 11x11 frame around the mouse pointer on the image. The famous Lenna image was chosen for this endeavour.

When running the sub-problem `FormulationOne.one()`, be careful to close the image by pressing the `ESC` key, and not by
clicking the 'x', otherwise the process will freeze, and you will have to manually kill it. OpenCV's `imshow` function
was used to complete this first task.

For the second task, OpenCV's `calcHist` function was used to calculate the three histograms, and MatplotLib's `plot`
and `xlim` functions took care of plotting those histograms on the user's screen.

On the third task, the biggest challenge was to actually erase the previous drawn rectangles around the mouse pointer
as the user moved the mouse around. To do so, inside a `while` loop, the image was re-read and put in another variable,
which was shown with `cv.imshow` right after the mouse callback function was called, and the white rectangle was drawn.
The mouse callback function has the purpose of setting the coordinate values of the rectangle, 13 pixels wide around the
pointer to create a 11x11 frame, grabbing the values of red, green and blue colors, and printing all the required 
information on the user's terminal. These information are: pointer coordinates, BGR values and the intensity value on 
those coordinates, and mean and standard deviation values of grey level on the 11x11 frame, which were calculated with
Python's `mean` and `std` built-in functions for the object `img`.

The fourth task had no coding involved, but simply a discussion. Such discussion was registered on `FormulationOne.four`'s
docstring, and states as follows:

"
To discuss homogeneousity and inhomogeneousity in our case, it would be best to look at the histogram and standard
        deviation values only. Looking at the histogram, we would classify a homogeneous image as an image with a rather
        flat histogram, without high or low peeks. We should observe the three color level graph lines being equally
        distant from each other throughout the entire graph range. Now, looking at the standard deviation values, a
        window frame with low variance could be considered homogeneous. We could say that, the lower the variance, the
        more homogeneous the frame is. That is because, when we have a low standard deviation, the specific value does
        not differ too much from the average, thus leading to a homogeneous frame.
"

### Formulation 02


### Formulation 03
Python's Numpy library provides methods to calculate the 2D DFT and inverse 2D DFT. Those methods are `numpy.fft.fft2`
and `numpy.fft.ifft2`, respectively. To bring the DC component to the center, `numpy.fft.fftshift` was used, and 
`numpy.fft.ifftshift` was used to undo this operation to bring back the image to the spatial domain.

Task *a* led us to converting two images to the frequency domain, and getting hold of their amplitude and phase values.
Then we mixed those values, thus creating a new image, with the amplitude of Lenna, which was the first image, and the
phase of Baboon, which was the second. The observed result is an image that is hardly recognizable, but looking at its
edges and shadows, we can see that baboon contributed more to the final mix. A second test was made, getting baboon's
amplitudes and lenna's phases, and the resulting image shows shadows of lenna's hat and shoulder. Therefore, we can
safely conclude that the amplitude values contribute more to an image than the phase ones, but the latter cannot be simply
discarded, for the image without those makes too much little visual sense.

### Formulation 04
