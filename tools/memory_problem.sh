# install the required packages
pip install memory_profiler
pip install matplotlib

# run the profiler to record the memory usage
# sample 0.1s by defaut
mprof run --include-children python fantastic_model_building_code.py

# plot the recorded memory usage
mprof plot --output memory-profile.png