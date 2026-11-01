import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../models/map_models.dart';

class MapMarkerLayerWidget extends StatelessWidget {
  const MapMarkerLayerWidget({super.key, required this.markers});

  final List<MapMarkerData> markers;

  @override
  Widget build(BuildContext context) {
    return MarkerLayer(
      markers: markers.map(_buildMarker).toList(),
    );
  }

  Marker _buildMarker(MapMarkerData m) {
    final color = _colorForType(m.type);
    final icon = _iconForType(m.type);

    return Marker(
      point: m.position,
      width: 44,
      height: 44,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
              border: Border.all(color: Colors.white, width: 2),
              boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 4)],
            ),
            child: Icon(icon, color: Colors.white, size: 20),
          ),
          if (m.label != null)
            Container(
              margin: const EdgeInsets.only(top: 2),
              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
              decoration: BoxDecoration(
                color: Colors.black87,
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                m.label!,
                style: const TextStyle(color: Colors.white, fontSize: 9),
              ),
            ),
        ],
      ),
    );
  }

  Color _colorForType(MapMarkerType type) {
    switch (type) {
      case MapMarkerType.user:
        return const Color(0xFF2563EB);
      case MapMarkerType.source:
        return const Color(0xFF16A34A);
      case MapMarkerType.destination:
        return const Color(0xFF7C3AED);
      case MapMarkerType.ambulance:
      case MapMarkerType.driver:
        return const Color(0xFFDC2626);
      case MapMarkerType.hospital:
        return const Color(0xFF0EA5E9);
    }
  }

  IconData _iconForType(MapMarkerType type) {
    switch (type) {
      case MapMarkerType.user:
        return Icons.person_pin_circle;
      case MapMarkerType.source:
        return Icons.location_on;
      case MapMarkerType.destination:
        return Icons.local_hospital;
      case MapMarkerType.ambulance:
      case MapMarkerType.driver:
        return Icons.local_shipping;
      case MapMarkerType.hospital:
        return Icons.medical_services;
    }
  }
}
