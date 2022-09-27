import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
# import cv2
from shapely.geometry import LinearRing, Polygon, Point

# from skimage.draw import polygon as poly

class Beam:
    """
    A class representing each beam.
    """

    # def __init__(self, ID, gantry_angle=None, collimator_angle=None, iso_center=None, beamlet_map_2d=None,
    #              BEV_structure_mask=None, beamlet_width_mm=None, beamlet_height_mm=None, beam_modality=None, MLC_type=None):
    def __init__(self, data):
        self.ID = data['ID']
        self.gantry_angle = data['gantry_angle']
        self.collimator_angle = data['collimator_angle']
        self.iso_center = data['iso_center']
        self.jaw_position = data['jaw_position']
        beamlet_opt = np.multiply(data['BEV_2d_beamlet_idx'], data['BEV_2d_structure_mask']['PTV'])
        self.beamlet_opt_ID = beamlet_opt[np.nonzero(beamlet_opt)]
        self.beamlet_opt = [data['beamlets'][i] for i in self.beamlet_opt_ID]
        self.BEV_2d_beamlet_idx = data['BEV_2d_beamlet_idx']
        self.BEV_2d_structure_mask = data['BEV_2d_structure_mask']
        self.beam_modality = data['beam_modality']
        self.MLC_type = data['MLC_type']
        self.beam_modality = data['beam_modality']

    def plot_BEV_2d_structure_mask(self, organ=None):
        plt.matshow(self.BEV_2d_structure_mask[organ])


# class Beams:
#     """
#     A class representing beams.
#     """
#
#     # def __init__(self, ID, gantry_angle=None, collimator_angle=None, iso_center=None, beamlet_map_2d=None,
#     #              BEV_structure_mask=None, beamlet_width_mm=None, beamlet_height_mm=None, beam_modality=None, MLC_type=None):
#     def __init__(self, beams, opt_beamlets_PTV_margin_mm=None):
#         self.beams_dict = beams
#         if opt_beamlets_PTV_margin_mm is None:
#             opt_beamlets_PTV_margin_mm = 3
#         self.opt_beamlets_PTV_margin_mm = opt_beamlets_PTV_margin_mm
#
#     def plot_BEV_2d_structure_mask(self, beam_id=None, organ=None):
#         plt.matshow(self.get_BEV_2d_structure_mask(beam_id, organ))
#
#     def get_BEV_2d_structure_mask(self, beam_id=None, organ=None, margin=0):
#         # ind = np.where(np.array(self.beams_dict['ID']) == beam_id)
#         ind = self.beams_dict['ID'].index(beam_id)
#         if margin == 0:
#             a_mask = self.beams_dict['BEV_structure_contour_points'][ind][organ]
#         else:
#             mask = self.beams_dict['BEV_structure_contour_points'][ind][organ]
#             mask = mask.astype('uint8')
#             contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#             for count_num in range(len(contours)):
#                 polygon = []
#                 for i in contours[count_num]:
#                     polygon.append((i[0][0], i[0][1]))
#                 r = LinearRing(polygon)
#                 s = Polygon(r)
#                 t = Polygon(s.buffer(margin / 2.5).exterior, [r])
#
#                 if count_num == 0:
#                     a_mask = np.zeros(shape=mask.shape[0:2])  # original
#                 poly_coordinates = np.array(list(t.exterior.coords))
#                 rr, cc = poly(poly_coordinates[:, 0], poly_coordinates[:, 1], (mask.shape[1], mask.shape[0]))
#                 a_mask[cc, rr] = 1
#         return a_mask
#
#     def get_2d_beamlet_idx(self, beam_id=None, organ='PTV'):
#
#         # ind = np.where(np.array(self.beams_dict['ID']) == beam_id)
#         ind = self.beams_dict['ID'].index(beam_id)
#         mask = self.get_BEV_2d_structure_mask(beam_id=beam_id, organ=organ, margin=self.opt_beamlets_PTV_margin_mm)
#         idx_2d = np.multiply(self.beams_dict['BEV_2d_beamlet_idx'][ind] + 1, mask)
#         beam_map = np.int32(idx_2d) - np.int32(1)
#         return beam_map
#
#     def get_original_map(self, beam_map):
#         rowsNoRepeat = [0]
#         for i in range(1, np.size(beam_map, 0)):
#             if (beam_map[i, :] != beam_map[rowsNoRepeat[-1], :]).any():
#                 rowsNoRepeat.append(i)
#         colsNoRepeat = [0]
#         for j in range(1, np.size(beam_map, 1)):
#             if (beam_map[:, j] != beam_map[:, colsNoRepeat[-1]]).any():
#                 colsNoRepeat.append(j)
#         beam_map = beam_map[np.ix_(np.asarray(rowsNoRepeat), np.asarray(colsNoRepeat))]
#         return beam_map

class Beams:
    """
    A class representing beams.
    """

    # def __init__(self, ID, gantry_angle=None, collimator_angle=None, iso_center=None, beamlet_map_2d=None,
    #              BEV_structure_mask=None, beamlet_width_mm=None, beamlet_height_mm=None, beam_modality=None, MLC_type=None):
    def __init__(self, beams, opt_beamlets_PTV_margin_mm=None):
        self.beams_dict = beams
        if opt_beamlets_PTV_margin_mm is None:
            opt_beamlets_PTV_margin_mm = 3
        self.opt_beamlets_PTV_margin_mm = opt_beamlets_PTV_margin_mm

    def get_structure_mask_2dgrid(self, beam_id=None, organ='PTV', margin=None, orig_res=True):
        # ind = np.where(np.array(self.beams_dict['ID']) == beam_id)
        if margin is None:
            margin = self.opt_beamlets_PTV_margin_mm

        ind = self.beams_dict['ID'].index(beam_id)
        contours = self.beams_dict['BEV_structure_contour_points'][ind][organ]
        for count_num in range(len(contours)):
            polygon = []
            for j in contours[count_num]:
                polygon.append((j[0], j[1]))
            r = LinearRing(polygon)
            s = Polygon(r)
            if margin == 0:
                shapely_poly = s
            else:
                shapely_poly = Polygon(s.buffer(margin), [r])
            #             poly_coordinates = np.array(list(t.exterior.coords))
            beamlets = self.beams_dict['beamlets'][ind]
            x_positions = [sub['position_x_mm'] for sub in beamlets]
            y_positions = [sub['position_y_mm'] for sub in beamlets]
            x_min_max_sort = np.sort(np.unique(x_positions))
            y_max_min_sort = np.sort(np.unique(y_positions))[::-1]
            points = []
            for i in range(len(beamlets)):
                x_coord = beamlets[i]['position_x_mm']
                y_coord = beamlets[i]['position_y_mm']
                points.append(Point(x_coord, y_coord))

            valid_points = []
            valid_points.extend(filter(shapely_poly.contains, points))
            x_and_y = [(a.x, a.y) for a in valid_points]
            if orig_res:
                XX, YY = np.meshgrid(x_min_max_sort, y_max_min_sort)
                w_all = np.column_stack((x_positions, y_positions))
                if count_num == 0:
                    mask = np.zeros_like(XX, dtype=bool)
                for row in range(XX.shape[0]):
                    for col in range(XX.shape[1]):
                        ind = np.where((w_all[:, 0] == XX[row, col]) & (w_all[:, 1] == YY[row, col]))[0][0]

                        if (beamlets[ind]['position_x_mm'], beamlets[ind]['position_y_mm']) in x_and_y:
                            # beam_map[row, col] = beamlets[ind]['id']
                            mask[row, col] = True
        return mask

    def get_beamlet_idx_2dgrid(self, beam_id=None, organ='PTV', margin=None, orig_res=True):

        # ind = np.where(np.array(self.beams_dict['ID']) == beam_id)
        if margin is None:
            margin = self.opt_beamlets_PTV_margin_mm
        ind = self.beams_dict['ID'].index(beam_id)
        mask = self.get_structure_mask_2dgrid(beam_id=beam_id, organ=organ, margin=margin,
                                              orig_res=orig_res)
        beamlets = self.beams_dict['beamlets'][ind]
        if orig_res:
            x_positions = [sub['position_x_mm'] for sub in beamlets]  # get the left corner
            y_positions = [sub['position_y_mm'] for sub in beamlets]  # get the right corner
            x_min_max_sort = np.sort(np.unique(x_positions))
            y_max_min_sort = np.sort(np.unique(y_positions))[::-1]
            XX, YY = np.meshgrid(x_min_max_sort, y_max_min_sort)
            w_all = np.column_stack((x_positions, y_positions))
            beam_map = np.zeros_like(XX, dtype=int)
            for row in range(XX.shape[0]):
                for col in range(XX.shape[1]):
                    ind = np.where((w_all[:, 0] == XX[row, col]) & (w_all[:, 1] == YY[row, col]))[0][0]
                    # beam_map[row, col] = beamlets[ind]['id']+np.int(1)# adding one so that 0th beamlet is retained
                    beam_map[row, col] = ind + np.int(1)  # adding one so that 0th beamlet is retained
            beam_map = np.multiply(beam_map, mask)
            beam_map = beam_map - np.int(1)  # subtract one again to get original beamlets
            # opt_beamlets = beam_map[beam_map >= 0]
            # beam_map = self.sort_beamlets(beam_map)
        # idx_2d = np.multiply(self.beams_dict['BEV_2d_beamlet_idx'][ind] + 1, mask)
        # beam_map = np.int32(idx_2d) - np.int32(1)
        return beam_map

    def plot_structure_mask_2dgrid(self, beam_id=None, organ=None, margin=None):
        if margin is None:
            margin = self.opt_beamlets_PTV_margin_mm
        plt.matshow(self.get_structure_mask_2dgrid(beam_id=beam_id, organ=organ, margin=margin))

    def plot_beamlet_idx_2dgrid(self, beam_id=None, organ=None, margin=None):
        if margin is None:
            margin = self.opt_beamlets_PTV_margin_mm
        plt.matshow(self.get_beamlet_idx_2dgrid(beam_id=beam_id, organ=organ, margin=margin))


    @staticmethod
    def get_original_map(beam_map):
        rowsNoRepeat = [0]
        for i in range(1, np.size(beam_map, 0)):
            if (beam_map[i, :] != beam_map[rowsNoRepeat[-1], :]).any():
                rowsNoRepeat.append(i)
        colsNoRepeat = [0]
        for j in range(1, np.size(beam_map, 1)):
            if (beam_map[:, j] != beam_map[:, colsNoRepeat[-1]]).any():
                colsNoRepeat.append(j)
        beam_map = beam_map[np.ix_(np.asarray(rowsNoRepeat), np.asarray(colsNoRepeat))]
        return beam_map

    def get_beam_angle(self, beam_id=None):
        ind = self.beams_dict['ID'].index(beam_id)
        return self.beams_dict['gantry_angle'][ind]

    def get_collimator_angle(self, beam_id=None):
        ind = self.beams_dict['ID'].index(beam_id)
        return self.beams_dict['collimator_angle'][ind]

    def get_influence_matrix(self, beam_ids=None, is_sparse=True):
        beam_ids_list = beam_ids if isinstance(beam_ids, list) else [beam_ids]
        for i, beam_id in enumerate(beam_ids_list):
            ind = self.beams_dict['ID'].index(beam_id)
            beamlet_idx_2dgrid = self.get_beamlet_idx_2dgrid(beam_id=beam_id, organ='PTV')
            opt_beamlets = beamlet_idx_2dgrid[beamlet_idx_2dgrid >= 0]
            if is_sparse:
                if i == 0:
                    inf_matrix = self.beams_dict['influenceMatrixSparse'][ind][:, opt_beamlets]
                else:
                    inf_matrix = sp.sparse.hstack([inf_matrix, self.beams_dict['influenceMatrixSparse'][ind][:, opt_beamlets]], format='csr')

        return inf_matrix


    # def add_beam(self, beam_id=None, *args, **kwargs):
    #     old_ids = self.beams_dict['ID']
    #     new_ids = old_ids.append(beam_id)
    #     plan = Plan(beam_indices=new_ids, *args, **kwargs)


    # since instance method can modify the class variables
    @staticmethod
    def sort_beamlets(b_map):
        c = b_map[b_map >= 0]
        ind = np.arange(0, len(c))
        c_sort = np.sort(c)
        matrix_ind = [np.where(b_map == c_i) for c_i in c_sort]
        map_copy = b_map.copy()
        for i in range(len(ind)):
            map_copy[matrix_ind[i]] = ind[i]
        return map_copy

    def get_optimization_beamlets(self, beam_ids=None, organ='PTV'):
        if beam_ids is None:
            beam_ids = self.beams_dict['ID']
        beam_ids_list = beam_ids if isinstance(beam_ids, list) else [beam_ids]

        all_beam_ids = self.beams_dict['ID']
        beam_extra_info = {}

        for i, get_id in enumerate(all_beam_ids):
            beamlets_2d_grid = self.get_beamlet_idx_2dgrid(beam_id=get_id, organ=organ)
            map = self.sort_beamlets(beamlets_2d_grid)
            std_beamlets = map[map >= 0]
            start_beamlet = np.sort(std_beamlets)[0]
            last_beamlet = np.sort(std_beamlets)[-1]
            if i == 0:
                beam_extra_info.setdefault('ID', []).append(get_id)
                beam_extra_info.setdefault('start_beamlet', []).append(start_beamlet)
                beam_extra_info.setdefault('end_beamlet', []).append(last_beamlet)

            else:
                prev_ind = beam_extra_info['end_beamlet'][i-1]
                beam_extra_info.setdefault('start_beamlet', []).append(prev_ind+start_beamlet)
                beam_extra_info.setdefault('end_beamlet', []).append(prev_ind+last_beamlet)
        opt_beamlets = np.array([])
        for beam_id in beam_ids_list:
            ind = beam_extra_info['ID'].index(beam_id)
            np.append(opt_beamlets, np.arange(beam_extra_info['start_beamlet'][ind], beam_extra_info['start_beamlet'][ind]+1))
        return opt_beamlets


    # def plot_2d_beamlet_intensity(self, x, beam_id=None, orig_res=True):
    #     beamlets_2d_grid = self.get_beamlet_idx_2dgrid(beam_id=beam_id, organ='PTV', orig_res=orig_res)

