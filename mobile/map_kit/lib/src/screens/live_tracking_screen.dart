import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';

import '../controllers/map_controller.dart';
import '../controllers/tracking_controller.dart';
import '../services/map_service.dart';
import '../widgets/emergency_map_widget.dart';

/// Live ambulance tracking with WebSocket + auto route refresh.
class LiveTrackingScreen extends StatefulWidget {
  const LiveTrackingScreen({
    super.key,
    required this.mapService,
    required this.emergencyId,
    required this.patientLocation,
    this.destinationLocation,
    this.onSendDriverGps,
  });

  final MapService mapService;
  final String emergencyId;
  final LatLng patientLocation;
  final LatLng? destinationLocation;

  /// Driver app: callback to POST GPS to Django API
  final Future<void> Function(LatLng position)? onSendDriverGps;

  @override
  State<LiveTrackingScreen> createState() => _LiveTrackingScreenState();
}

class _LiveTrackingScreenState extends State<LiveTrackingScreen> {
  late final EmergencyMapController _mapController;
  TrackingController? _trackingController;

  @override
  void initState() {
    super.initState();
    _mapController = EmergencyMapController(widget.mapService);
    _start();
  }

  Future<void> _start() async {
    await _mapController.initialize();
    _mapController.setSourceDestination(
      source: widget.patientLocation,
      destination: widget.destinationLocation ??
          LatLng(
            widget.patientLocation.latitude + 0.02,
            widget.patientLocation.longitude + 0.02,
          ),
    );

    _trackingController = TrackingController(
      mapService: widget.mapService,
      mapController: _mapController,
      emergencyId: widget.emergencyId,
      patientLocation: widget.patientLocation,
      destinationLocation: widget.destinationLocation,
    );
    await _trackingController!.start();

    if (widget.onSendDriverGps != null) {
      widget.mapService.location.watchPosition(distanceFilterMeters: 10).listen((pos) {
        widget.onSendDriverGps!(pos);
      });
    }

    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    _trackingController?.dispose();
    _mapController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final eta = _trackingController?.state.etaMinutes;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Live Tracking'),
        backgroundColor: const Color(0xFFDC2626),
        foregroundColor: Colors.white,
      ),
      body: Stack(
        children: [
          EmergencyMapWidget(
            controller: _mapController,
            initialCenter: widget.patientLocation,
          ),
          Positioned(
            left: 16,
            right: 16,
            top: 12,
            child: Material(
              elevation: 4,
              borderRadius: BorderRadius.circular(12),
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Row(
                  children: [
                    const Icon(Icons.local_shipping, color: Color(0xFFDC2626)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('Ambulance en route', style: TextStyle(fontWeight: FontWeight.bold)),
                          Text(
                            eta != null ? 'ETA: $eta min' : 'Calculating route...',
                            style: TextStyle(color: Colors.grey[600], fontSize: 13),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xFFDC2626).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Text('LIVE', style: TextStyle(color: Color(0xFFDC2626), fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
