import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';

import '../controllers/map_controller.dart';
import '../services/map_service.dart';
import '../widgets/emergency_map_widget.dart';

/// General map: user location, nearby hospitals/ambulances, optional route preview.
class MapScreen extends StatefulWidget {
  const MapScreen({
    super.key,
    required this.mapService,
    this.source,
    this.destination,
  });

  final MapService mapService;
  final LatLng? source;
  final LatLng? destination;

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late final EmergencyMapController _controller;

  @override
  void initState() {
    super.initState();
    _controller = EmergencyMapController(widget.mapService);
    _init();
  }

  Future<void> _init() async {
    await _controller.initialize();
    if (widget.source != null && widget.destination != null) {
      _controller.setSourceDestination(
        source: widget.source!,
        destination: widget.destination!,
      );
      await _controller.drawRoute(widget.source!, widget.destination!);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Emergency Map'),
        actions: [
          IconButton(
            icon: const Icon(Icons.layers),
            onPressed: _controller.toggleDarkMode,
          ),
        ],
      ),
      body: EmergencyMapWidget(controller: _controller),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _controller.centerOnUser,
        icon: const Icon(Icons.my_location),
        label: const Text('My location'),
      ),
    );
  }
}
