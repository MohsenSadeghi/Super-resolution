import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def path_length (p, d):
	
	s = p.shape
	
	dist_tot = 0.0
	
	for i in range(s[0] - 1):
		dist_tot += d[p[i], p[i + 1]]
	
	return dist_tot

def Boltzmann_prob (dE, beta):

	acc = False
	
	if dE < 0.0:
		acc = True
	else:
		ch = np.random.random_sample ()
		if ch < np.exp (-beta * dE):
			acc = True
	
	return acc

def RandInt (n):
	
	return int (np.floor (np.random.random_sample () * n))
	
def main ():
	
	frames_padded = np.load('../149septin_rotated.npy')
	d = np.load('../149septin_dist.npy')

	n_frames_tot, lx, ly = frames_padded.shape
			
	#plt.matshow (d)
	
	#plt.draw ()
	
	#plt.show ()
	
	n_steps = int(2e6)
	beta = 5.0e3
	n_paths = 10
	
	path = []
	path_0 = np.arange (0, n_frames_tot)
	
	path.append(path_0)

	for i in range (n_paths):
		path.append(np.array([], dtype=int))
	
	current_dist = 0.0
	
	for i in range (n_paths):
		current_dist += path_length (path[i], d)
	
	dist_history = np.zeros ([n_steps, 1])
	
	for step in range (n_steps):
		
		beta += 0.1

		step_type = RandInt (2)
		
		if step_type == 0:
			
			path_ind = RandInt (n_paths)
			n_frames_in_path = path[path_ind].shape[0]
			
			if n_frames_in_path > 0:
				
				ind1 = RandInt (n_frames_in_path)
				ind2 = RandInt (n_frames_in_path)
						
				delta_dist = 0.0
				
				if ind1 != ind2:
					
					if ind1 > 0:
						delta_dist -= d[path[path_ind][ind1 - 1], path[path_ind][ind1]]
						delta_dist += d[path[path_ind][ind1 - 1], path[path_ind][ind2]]

					if ind1 < n_frames_in_path - 1:
						delta_dist -= d[path[path_ind][ind1], path[path_ind][ind1 + 1]]
						delta_dist += d[path[path_ind][ind2], path[path_ind][ind1 + 1]]

					if ind2 > 0:
						delta_dist -= d[path[path_ind][ind2 - 1], path[path_ind][ind2]]
						delta_dist += d[path[path_ind][ind2 - 1], path[path_ind][ind1]]

					if ind2 < n_frames_in_path - 1:
						delta_dist -= d[path[path_ind][ind2], path[path_ind][ind2 + 1]]
						delta_dist += d[path[path_ind][ind1], path[path_ind][ind2 + 1]]
					
					if np.abs (ind1 - ind2) == 1:
						delta_dist += 2.0 * d[path[path_ind][ind1], path[path_ind][ind2]]
		
							
					if Boltzmann_prob (delta_dist, beta):
						
						path[path_ind][ind1], path[path_ind][ind2] = path[path_ind][ind2], path[path_ind][ind1]

						current_dist += delta_dist
						
		if step_type == 1:
			
			path_ind1 = RandInt (n_paths)
			path_ind2 = RandInt (n_paths)

			n_frames_in_path1 = path[path_ind1].shape[0]
			n_frames_in_path2 = path[path_ind2].shape[0]
			
			if (n_frames_in_path1 > 0) and (path_ind1 != path_ind2):

				ind1 = RandInt (n_frames_in_path1)
				ind2 = RandInt (n_frames_in_path2 + 1)
						
				delta_dist = 0.0

				if ind1 > 0:
					delta_dist -= d[path[path_ind1][ind1 - 1], path[path_ind1][ind1]]

				if ind1 < n_frames_in_path1 - 1:
					delta_dist -= d[path[path_ind1][ind1], path[path_ind1][ind1 + 1]]
					
				if (ind1 > 0) and (ind1 < n_frames_in_path1 -1):
					delta_dist += d[path[path_ind1][ind1 - 1], path[path_ind1][ind1 + 1]]
				
				if n_frames_in_path2 > 0:

					if ind2 == 0:
						delta_dist += d[path[path_ind1][ind1], path[path_ind2][0]]
					elif ind2 == n_frames_in_path2:
						delta_dist += d[path[path_ind1][ind1], path[path_ind2][n_frames_in_path2 - 1]]
					elif (ind2 < n_frames_in_path2) and (ind2 > 0):
						delta_dist += d[path[path_ind1][ind1], path[path_ind2][ind2 - 1]]
						delta_dist += d[path[path_ind1][ind1], path[path_ind2][ind2]]
						delta_dist -= d[path[path_ind2][ind2], path[path_ind2][ind2 - 1]]
					
				if Boltzmann_prob (delta_dist, beta):

					path[path_ind2] = np.insert (path[path_ind2], ind2, path[path_ind1][ind1])
					path[path_ind1] = np.delete (path[path_ind1], ind1)
					
					current_dist += delta_dist

		dist_history[step] = current_dist
			
	np.save ('../149septin_path', path)
	
	fig1 = plt.figure ()
	ax = fig1.gca ()
	
	ax.plot (dist_history)
	plt.show ()
					
	return ()

main ()
