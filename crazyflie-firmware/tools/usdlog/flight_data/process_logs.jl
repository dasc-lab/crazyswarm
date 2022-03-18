using Plots
using CSV
using DataFrames

# df = DataFrame(CSV.File("log00.csv"))
# time_inds = [s for s in 1:size(df,1)  if df[s,"tick"] > 2e5 && df[s, :tick] < 3.3e5]

# df = DataFrame(CSV.File("log01.csv"))
# time_inds = [s for s in 1:size(df, 1) if df[s,"tick"] > 4e4 && df[s, "tick"] < 4.77e4]

# df = DataFrame(CSV.File("log03.csv"))
# time_inds = [s for s in 1:size(df, 1) if df[s,"tick"] > 1e4 && df[s, "tick"] < 3e4]



df = DataFrame(CSV.File("mine.csv"))
time_inds = [s for s in 1:size(df,1)  if df[s,"tick"] > 4.5e4 && df[s, :tick] < 6.7e4]



ts = df[time_inds, "tick"]
xs = df[time_inds, "ctrlGeo.log_state_x"]
ys = df[time_inds, "ctrlGeo.log_state_y"]
zs = df[time_inds, "ctrlGeo.log_state_z"]


plot(xs, ys)
vline!([0.5])
plot!(flip=true)

# plot(ts, zs)


savefig("plot.png")

# @show df