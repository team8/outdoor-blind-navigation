import object_filter as of

obs = [('knife', '30.26', (250.02488708496094, 85.19881439208984, 62.963951110839844, 129.86805725097656)), ('scissors', '34.59', (246.94873046875, 83.70958709716797, 59.21462631225586, 127.32121276855469))]
print(obs[0][2])
print(of.compute_iou(obs[0][2], obs[0][2]))
