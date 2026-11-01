import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import '../models/map_models.dart';

class RoutePolylineLayer extends StatelessWidget {
  const RoutePolylineLayer({super.key, required this.route});

  final RouteSegment? route;

  @override
  Widget build(BuildContext context) {
    if (route == null || route!.points.length < 2) {
      return const SizedBox.shrink();
    }

    return PolylineLayer(
      polylines: [
        // Emergency highlight: outer glow
        if (route!.isEmergency)
          Polyline(
            points: route!.points,
            color: const Color(0xFFDC2626).withValues(alpha: 0.35),
            strokeWidth: 12,
          ),
        Polyline(
          points: route!.points,
          color: route!.isEmergency ? const Color(0xFFDC2626) : const Color(0xFF2563EB),
          strokeWidth: route!.isEmergency ? 6 : 4,
          borderColor: Colors.white,
          borderStrokeWidth: 2,
        ),
      ],
    );
  }
}
