import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
	
def dist (f1, f2):
	
	return np.sum(np.power((f1-f2).reshape((-1,1)),2))

def main ():
			
	frames_padded = np.load('../149septin_rotated.npy')

	n_frames, lx, ly = frames_padded.shape
	
	d = np.zeros ([n_frames, n_frames]);
	
	for i in range(n_frames):
		for j in range(i + 1, n_frames):
			d[i, j] = dist (frames_padded[i], frames_padded[j])
			d[j, i] = d[i, j]
	
	plt.matshow (d)
	
	plt.draw ()
	
	plt.show ()
	
	np.save ('../149septin_dist', d)
	
	return ()

main ()
