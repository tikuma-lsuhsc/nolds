from . import measures as nolds

def plot_lyap():
	import matplotlib.pyplot as plt # local import to avoid dependency for non-debug use
	rvalues = np.arange(2, 4, 0.01)
	lambdas = []
	lambdas_est = []
	lambdas_est2 = []
	maps = []
	logistic = lambda x : r * x * (1 - x)
	for r in rvalues:
		x = 0.1
		result = []
		full_data = [x]
		# ignore first 100 values for bifurcation plot
		for t in range(100):
			x = logistic(x)
			tmp = abs(r-2*r*x)
			dx = np.nan if tmp <= 0 else np.log(tmp)
			result.append(dx)
			full_data.append(x)
		lambdas.append(np.mean(result))
		for t in range(20):
			x = logistic(x)
			maps.append(x)
			full_data.append(x)
		le = nolds.lyap_e(np.array(full_data), emb_dim=6, matrix_dim=2)
		lambdas_est.append(np.max(le))
		lambdas_est2.append(nolds.lyap_r(np.array(full_data), emb_dim=6, lag=2, min_tsep=10, trajectory_len=20))
	plt.title("Lyapunov exponent of the logistic map")
	plt.plot(rvalues, lambdas, "b-", label="true lyap. exponent")
	plt.plot(rvalues, lambdas_est, color="#00AAAA", label="estimation using lyap_e")
	plt.plot(rvalues, lambdas_est2, color="#AA00AA", label="estimation using lyap_r")
	plt.plot(rvalues, np.zeros(len(rvalues)), "g--")
	xvals = np.repeat(rvalues, 20)
	plt.plot(xvals, maps, "ro", alpha=0.1, label="bifurcation plot")
	plt.ylim((-2,2))
	plt.xlabel("r")
	plt.ylabel("lyap. exp / logistic(x, r)")
	plt.legend(loc="best")
	plt.show()

def profiling():
	import cProfile
	n = 10000
	data = np.cumsum(np.random.random(n)-0.5)
	cProfile.runctx('lyap_e(data)',{'lyap_e': lyap_e},{'data': data})

if __name__ == "__main__":
	import sys
	if sys.argv[1] == "all" or len(sys.argv) == 1:
		plot_lyap()
	elif sys.argv[1] == "lyapunov":
		plot_ylap()
	elif sys.argv[1] == "profiling":
		profiling()