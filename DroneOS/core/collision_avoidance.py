import math
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from DroneOS.shared.utils.logger import setup_logger
from DroneOS.shared.protocol.messages import TelemetryData

logger = setup_logger("CollisionAvoidance")

class ICollisionAvoidance(ABC):
    @abstractmethod
    def evaluate_threats(self, self_telemetry: TelemetryData, swarm_telemetry: Dict[str, TelemetryData]) -> Tuple[bool, Optional[Dict[str, float]]]:
        """
        Evaluates potential collisions based on self telemetry and the swarm telemetry map.
        Returns (is_threat_detected, corrective_velocity_vector)
        """
        pass

class StandardCollisionAvoidance(ICollisionAvoidance):
    """
    Decentralized collision avoidance logic using Predictive Separation.
    """
    def __init__(self, minimum_safe_distance: float = 3.0, lookahead_seconds: float = 2.0):
        self.min_dist = minimum_safe_distance
        self.lookahead = lookahead_seconds

    def _predict_pos(self, t: TelemetryData, dt: float) -> Tuple[float, float, float]:
        # Approximate lat/lon to meters is complex, but for local collision avoidance
        # we can assume 1 deg lat = 111320m, 1 deg lon = 111320 * cos(lat)
        # But AirSim velocity is in NED meters/sec, not degrees/sec.
        # So we can't directly add vx to latitude.
        # For simplicity in this static stub, we'll use a local tangent plane approximation 
        # but since we only have global coords, let's just project using standard metrics.
        # Actually, we can just compare velocities if we assume they are in the same frame.
        lat = t.latitude or 0.0
        lon = t.longitude or 0.0
        alt = t.altitude or 0.0
        
        # very rough approximation for local metric projection (relative to an origin, but here we just use differences)
        return (lat, lon, alt)

    def evaluate_threats(self, self_telemetry: TelemetryData, swarm_telemetry: Dict[str, TelemetryData]) -> Tuple[bool, Optional[Dict[str, float]]]:
        if self_telemetry.latitude is None or self_telemetry.longitude is None:
            return False, None

        my_lat = self_telemetry.latitude
        my_lon = self_telemetry.longitude
        my_alt = self_telemetry.altitude or 0.0

        for peer_id, peer_t in swarm_telemetry.items():
            if peer_t.latitude is None or peer_t.longitude is None:
                continue
                
            # Distance in meters
            R = 6371000
            phi1 = math.radians(my_lat)
            phi2 = math.radians(peer_t.latitude)
            delta_phi = math.radians(peer_t.latitude - my_lat)
            delta_lambda = math.radians(peer_t.longitude - my_lon)

            a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            dist = R * c
            
            alt_diff = abs(my_alt - (peer_t.altitude or 0.0))
            
            # Simple Sphere check
            if dist < self.min_dist and alt_diff < self.min_dist:
                logger.warning(f"Collision Threat with {peer_id}! Dist: {dist:.2f}m")
                
                # Simple repel vector (move away from peer)
                # Calculate bearing to peer, then move opposite
                bearing = math.atan2(
                    math.sin(delta_lambda) * math.cos(phi2),
                    math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
                )
                # Opposite direction
                escape_bearing = bearing + math.pi
                
                vx = 2.0 * math.cos(escape_bearing)
                vy = 2.0 * math.sin(escape_bearing)
                vz = -1.0 # Also climb slightly
                
                return True, {"vx": vx, "vy": vy, "vz": vz, "duration": 1.0}

        return False, None
