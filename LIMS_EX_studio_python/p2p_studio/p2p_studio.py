import os
import numpy as np
import csv
from isaacsim.core.api import SimulationContext
from isaacsim.core.utils.types import ArticulationAction
from .via_point_manager import IRIMCubicHermiteSpline
from ..global_variables import LIMS_EX_JOINT_NAMES
np.set_printoptions(suppress=True, precision=3, linewidth=100) 

class P2PStudio:
    def __init__(self, ui_builder, traj_dir, p2p_name_field):
        self._ui_builder = ui_builder
        self._traj_dir = traj_dir
        self._p2p_name_field = p2p_name_field 
        self.via_points_cache = []

        # P2P Play 관련 변수들
        self._p2p_data = [] 
        self._current_via_idx = 0
        self._segment_time = 0.0
        self._spline = None
        self._playback_active = False

    def on_p2p_play_clicked(self):
        try:
            folder_name = self._p2p_name_field.model.get_value_as_string().strip()
            if not folder_name:
                print("⚠️ Folder name을 입력하세요.")
                return
            
            csv_path = os.path.join(self._traj_dir, folder_name + "_group", "lims_ex_viapoints.csv")
            if not os.path.exists(csv_path):
                print(f"❌ CSV 파일 없음: {csv_path}")
                return
            
            # 3. 데이터 파싱 (한번에 처리)
            self._p2p_data = []
            with open(csv_path, "r") as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 스킵
                for row in reader:
                    if len(row) > 1:
                        duration = float(row[0])
                        positions = np.array([float(val) for val in row[1:]]) * np.pi / 180.0  # deg2rad
                        self._p2p_data.append((duration, positions))
            
            if not self._p2p_data:
                print("❌ 유효한 데이터가 없습니다.")
                return
            
            # 4. 재생 초기화
            self._current_via_idx = 0
            self._segment_time = 0.0
            self._spline = None
            
            # 5. 콜백 설정
            sim_ctx = SimulationContext.instance()
            if self._playback_active:
                sim_ctx.remove_physics_callback("p2p_playback")

            def playback_step(step_dt):
                articulation = self._ui_builder._scenario._articulation
                if not articulation or self._current_via_idx >= len(self._p2p_data):
                    sim_ctx.remove_physics_callback("p2p_playback")
                    self._playback_active = False
                    print("✅ P2P Playback 완료")
                    return
                
                # 현재 구간 정보
                duration, target_pos = self._p2p_data[self._current_via_idx]
                
                # 스플라인 생성 (한번만)
                if self._spline is None:
                    current_pos = articulation.get_joint_positions()[:len(LIMS_EX_JOINT_NAMES)]
                    self._spline = IRIMCubicHermiteSpline(len(LIMS_EX_JOINT_NAMES))
                    self._spline.add_back_via_point(0.0, current_pos)
                    self._spline.add_back_via_point(0.0, current_pos)  
                    self._spline.add_back_via_point(duration, target_pos)
                    self._spline.add_back_via_point(0.0, target_pos)
                
                # 시간 업데이트 및 보간
                self._segment_time += step_dt
                t_ms = min(self._segment_time, duration) * 1000.0
                
                _, positions, velocities = self._spline.get_target(t_ms)
                if positions is not None:
                    # 전체 DOF 위치 구성
                    all_positions = articulation.get_joint_positions().copy()
                    all_positions[:len(LIMS_EX_JOINT_NAMES)] = positions
                    
                    action = ArticulationAction(
                        joint_positions=all_positions,
                        joint_velocities=velocities if velocities is not None else None
                    )
                    articulation.apply_action(action)
                
                # 다음 구간으로 이동
                if self._segment_time >= duration:
                    self._current_via_idx += 1
                    self._segment_time = 0.0
                    self._spline = None
            
            sim_ctx.add_physics_callback("p2p_playback", playback_step)
            self._playback_active = True
            print(f"▶️ P2P Playback 시작: {len(self._p2p_data)} via points")
            
        except Exception as e:
            print(f"❌ P2P Play error: {e}")

    def on_via_point_clicked(self):
        articulation = self._ui_builder._scenario._articulation
        if articulation is None:
            print("❌ Articulation not ready")
            return

        joint_positions = articulation.get_joint_positions()[:len(LIMS_EX_JOINT_NAMES)]
        self.via_points_cache.append(np.array((joint_positions)))

        degrees_rounded = np.degrees(self.via_points_cache).round(3).tolist()
        print(f"✅ Via Point 추가: {len(self.via_points_cache)}")
        for i, point in enumerate(degrees_rounded):
            formatted_point = [f"{val:.3f}" for val in point]  # 소수점 3자리 문자열로 변환
            print(f"Point {i+1}: {formatted_point}")
        print("\n")

    def on_clear_clicked(self):
        self.via_points_cache = []
        print("✅ Via Point 리스트 초기화")

    def on_via_point_save_clicked(self):
        folder_name = self._p2p_name_field.model.get_value_as_string().strip()
        if not folder_name:
            print("⚠️ Folder name을 입력하세요.")
            return

        folder_path = os.path.join(self._traj_dir, folder_name + "_group")
        articulation = self._ui_builder._scenario._articulation
        if articulation is None:
            print("❌ Articulation not ready")
            return

        # 폴더 생성
        os.makedirs(folder_path, exist_ok=True)

        # CSV 파일 경로
        csv_path = os.path.join(folder_path, 'lims_ex_viapoints.csv')
        
        # 조인트 이름을 인덱스로 매핑
        joint_names_all = articulation.dof_names
        indices = [joint_names_all.index(joint) for joint in LIMS_EX_JOINT_NAMES]
        
        # CSV 파일 작성
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # 헤더 작성: duration + 실제 조인트 이름들
            header = ["duration"] + LIMS_EX_JOINT_NAMES
            writer.writerow(header)
            
            # 데이터 작성
            for via_point in self.via_points_cache:
                row = [3.0] + [round(np.degrees(via_point[idx]), 3) for idx in indices]
                writer.writerow(row)
        
        print(f"✅ Via Point가 {csv_path}에 저장되었습니다.")

    def on_remove_clicked(self):
        if not self.via_points_cache:
            print("⚠️ 삭제할 Via Point가 없습니다.")
            return
        
        self.via_points_cache.pop()
        print(f"❌ Via Point 삭제: {len(self.via_points_cache)}")
        for i, point in enumerate(np.degrees(self.via_points_cache).round(3).tolist()):
            formatted_point = [f"{val:.3f}" for val in point]
            print(f"Point {i+1}: {formatted_point}")
        print("\n")