import subprocess as sp

import cv2
import numpy as np


def make_ls_list(input_path):
    ls_cmd = "ls %s" % input_path
    proc = sp.Popen(ls_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    std_out, std_err = proc.communicate()
    ls_file_name = std_out.decode('utf-8').rstrip().split('\n')
    print(ls_cmd)
    return ls_file_name


def brighten_shadows(image_path, output_path, file_name):
    image_path = image_path + file_name
    output_path = output_path + file_name

    # 画像を読み込み
    image = cv2.imread(image_path)
    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 影とみなされる輝度の閾値を設定
    _, shadow_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    shadow_mask = shadow_mask.astype(bool)

    # 元の画像をコピー
    brightened_image = image.copy()

    # 影の部分の輝度を増加させる
    # HSV色空間を使って輝度(Hue, Saturation, Value)を調整
    hsv_image = cv2.cvtColor(brightened_image, cv2.COLOR_BGR2HSV)
    value_scale = 2  # 輝度をどれだけ増やすかの係数
    hsv_image[shadow_mask, 2] = np.clip(hsv_image[shadow_mask, 2] * value_scale, 0, 255)

    # HSVからBGRに変換
    brightened_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # 処理した画像を保存
    cv2.imwrite(output_path, brightened_image)
    print(f"Image saved to {output_path}")

    return brightened_image


def get_args():
    additional_path = ''
    input_path = 'images/input/winter_building_GSD4/' + additional_path
    output_path = 'images/output/winter_building_GSD4/' + additional_path
    return input_path, output_path


def main():
    input_path, output_path = get_args()
    ls_file_name = make_ls_list(input_path)
    for file_name in ls_file_name:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print('Prosessing file name is : ', file_name)
        brighten_shadows(input_path, output_path, file_name)


if __name__ == '__main__':
    main()
