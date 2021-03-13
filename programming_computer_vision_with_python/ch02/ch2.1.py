from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters


def compute_harris_response(im, sigma=3):
    """
    在一副灰度图像，对每个像素计算Harris角点检测器响应函数
    :param im:
    :param sigma:
    :return:
    """
    # 计算导数
    imx = zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (0, 1), imx)
    imy = zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (1, 0), imy)

    # 计算Harris矩阵的分量
    Wxx = filters.gaussian_filter(imx * imx, sigma)
    Wxy = filters.gaussian_filter(imx * imy, sigma)
    Wyy = filters.gaussian_filter(imy * imy, sigma)

    # 计算特征值和迹
    # 迹：一个 n * n 矩阵A主对角线所有元素之和
    Wdet = Wxx * Wyy - Wxy ** 2
    Wtr = Wxx + Wyy

    return Wdet / Wtr


def get_harris_points(harrisim, min_dist=10, thresold=0.01):
    """
    从一幅Harris响应图像中返回角点。
    min_dist为分割角点和图像边界的最少像素数目
    :param harrisim:
    :param min_dist:
    :param thresold:
    :return:
    """
    # 寻找高于阈值的的候选角点
    corner_thresold = harrisim.max() * thresold
    harrisim_t = (harrisim > corner_thresold) * 1

    # 得到候选点的坐标
    coords = array(harrisim_t.nonzero()).T

    # 以及它们的Harris响应值
    condidate_values = [harrisim[c[0], c[1]] for c in coords]

    # 对候选点按照Harris响应值进行排序
    index = argsort(condidate_values)

    # 将可行点的位置保存到数组中
    allowed_locations = zeros(harrisim.shape)
    allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 1

    # 按照min_distance原则，选择最佳Harris点
    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i, 0], coords[i, 1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i, 0] - min_dist):(coords[i, 0] + min_dist),
            (coords[i, 1] - min_dist):(coords[i, 1] + min_dist)] = 0
    return filtered_coords


def plot_harris_points(image, filtered_coords):
    """
    绘制图像中检测到的角点
    :param image:
    :param filtered_coords:
    :return:
    """
    figure()
    gray()
    imshow(image)
    plot([p[1] for p in filtered_coords], [p[0] for p in filtered_coords], '*')
    axis('off')
    show()


def get_descriptors(image, filtered_coords, wid=5):
    """
    对于每个返回的点，返回点周围 2 * wid + 1 个像素的值（假设选点的min_distance > wid）
    :param image:
    :param filtered_coords:
    :param wid:
    :return:
    """


if __name__ == '__main__':
    im = array(Image.open('../resource/picture/empire.jpg').convert('L'))
    harrisim = compute_harris_response(im)
    filtered_coords = get_harris_points(harrisim, 6, 0.1)
    plot_harris_points(im, filtered_coords)
