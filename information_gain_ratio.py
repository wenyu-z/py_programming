# Reference
# http://www.ke.tu-darmstadt.de/lehre/archiv/ws0809/mldm/dt.pdf

def calc_var_entropy(df, var):
    total_count = len(df)
    levels = df[var].unique()
    per_level_count = df.groupby(by=var).agg('count').values[:,0]
    prob = map(lambda x: x/float(total_count), per_level_count)
    neglog = map(lambda x: -x*np.log2(x), prob)
    entropy = reduce(lambda x,y: x+y, neglog)
    return entropy

def gain_ratio(df, features, target):
    total_count = len(df)
    target_entropy = calc_var_entropy(df, target)
    gain_ratio_df = pd.DataFrame(columns=['feature', 'gain_ratio'])
    
    for feat in features:
        target_entropy_per_feat_level = df.groupby(by = feat).apply(lambda dfnow: calc_var_entropy(dfnow, target)).values
        per_level_count = df.groupby(by = feat).agg('count').values[:,0]
        prob = map(lambda x: x/float(total_count), per_level_count)
        neglog = map(lambda (prob_this_level, target_entropy_this_level): -prob_this_level*target_entropy_this_level,
                         zip(prob, target_entropy_per_feat_level))
        gain = target_entropy + np.sum(neglog)
        split_info = calc_var_entropy(df, feat)
        gain_ratio = gain/float(split_info)
        gain_ratio_df = pd.concat((gain_ratio_df,
                                  pd.DataFrame(columns=['feature', 'gain_ratio'],
                                              data = [(feat, gain_ratio)])))
    gain_ratio_df.sort_values(by = ['gain_ratio'], ascending = False, inplace = True)
    gain_ratio_df.reset_index(inplace = True, drop = True)
    return gain_ratio_df
