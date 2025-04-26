from torch.utils.tensorboard import SummaryWriter

log_dir = "./logs/test"
writer = SummaryWriter(log_dir)
for i in range(10):
    writer.add_scalar("example/metric", i, i)
writer.close()