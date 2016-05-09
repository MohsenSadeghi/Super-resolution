import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def path_length (p, d):
	
	s = p.shape
	
	dist_tot = 0.0
	
	for i in range(s[0] - 1):
		dist_tot += d[p[i], p[i + 1]]
	
	return dist_tot
	
def main ():
			
	frames_padded = np.load('../149septin_rotated.npy')
	d = np.load('../149septin_dist.npy')

	n_frames, lx, ly = frames_padded.shape
			
	#plt.matshow (d)
	
	#plt.draw ()
	
	#plt.show ()
	
	n_steps = 10000000
	beta = 1.0e4
	
	path = np.arange (0, n_frames)
	path_test = np.arange (0, n_frames)

	current_dist = path_length (path, d)
	
	dist_history = np.zeros ([n_steps, 1])
	
	for step in range (n_steps):
		
		beta += 0.01
		
		ind1 = int (np.floor (np.random.random_sample () * n_frames))
		ind2 = int (np.floor (np.random.random_sample () * n_frames))
				
		delta_dist = 0.0
		
		if ind1 != ind2:
			
			if ind1 > 0:
				delta_dist -= d[path[ind1 - 1], path[ind1]]
				delta_dist += d[path[ind1 - 1], path[ind2]]

			if ind1 < n_frames - 1:
				delta_dist -= d[path[ind1], path[ind1 + 1]]
				delta_dist += d[path[ind2], path[ind1 + 1]]

			if ind2 > 0:
				delta_dist -= d[path[ind2 - 1], path[ind2]]
				delta_dist += d[path[ind2 - 1], path[ind1]]

			if ind2 < n_frames - 1:
				delta_dist -= d[path[ind2], path[ind2 + 1]]
				delta_dist += d[path[ind1], path[ind2 + 1]]
			
			if np.abs (ind1 - ind2) == 1:
				delta_dist += 2.0 * d[path[ind1], path[ind2]]
				
		dist_history[step] = current_dist
		
		accepted = False
		
		if delta_dist < 0.0:

			accepted = True

		else:

			ch = np.random.random_sample ()
	
			if ch < np.exp (-beta * delta_dist):
				accepted = True
				
		if accepted:
			
			path[ind1], path[ind2] = path[ind2], path[ind1]
			#print path_length (path, d)
			current_dist += delta_dist

	frames_sorted = frames_padded[path[:]]
	
	np.save ('../149septin_sorted', frames_sorted)

	for i in range(n_frames):
		
		plt.clf ()
		
		plt.imshow (frames_sorted[i])
			
		plt.pause (0.1)
		
		plt.draw ()

	fig1 = plt.figure ()
	ax = fig1.gca ()
	
	ax.plot (dist_history)
	plt.show ()
					
	return ()

main ()
