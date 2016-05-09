import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
	
def main ():
			
	frames_sorted = np.load('../149septin_sorted.npy')

	n_frames, lx, ly = frames_sorted.shape

	for i in range(n_frames):
		
		plt.clf ()
		
		plt.imshow (frames_sorted[i], cmap = plt.get_cmap('hot'))
			
		plt.pause (0.1)
		
		plt.draw ()
					
	return ()

main ()
