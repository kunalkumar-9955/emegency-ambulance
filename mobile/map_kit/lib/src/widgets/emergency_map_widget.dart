import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart' as fm;
import 'package:latlong2/latlong.dart';

import '../controllers/map_controller.dart';
import 'map_marker_layer.dart';
import 'map_zoom_controls.dart';
import 'route_polyline_layer.dart';

/// Optimized OSM map: repaint boundaries, limited layers for low-end devices.
class EmergencyMapWidget extends StatelessWidget {
  const EmergencyMapWidget({
    super.key,
    required this.controller,
    this.showZoomControls = true,
    this.initialCenter,
    this.initialZoom = 14,
  });

  final EmergencyMapController controller;
  final bool showZoomControls;
  final LatLng? initialCenter;
  final double initialZoom;

  @override
  Widget build(BuildContext context) {
    final center = initialCenter ?? controller.userLocation ?? const LatLng(28.6139, 77.2090);

    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        return Stack(
          children: [
            fm.FlutterMap(
              mapController: controller.mapController,
              options: fm.MapOptions(
                initialCenter: center,
                initialZoom: initialZoom,
                interactionOptions: const fm.InteractionOptions(
                  flags: fm.InteractiveFlag.all & ~fm.InteractiveFlag.rotate,
                ),
              ),
              children: [
                controller.tileLayer,
                RepaintBoundary(child: RoutePolylineLayer(route: controller.activeRoute)),
                RepaintBoundary(child: MapMarkerLayerWidget(markers: List.from(controller.markers))),
              ],
            ),
            if (controller.isLoading)
              const Center(child: CircularProgressIndicator()),
            if (showZoomControls)
              Positioned(
                right: 12,
                bottom: 100,
                child: MapZoomControls(controller: controller),
              ),
          ],
        );
      },
    );
  }
}
