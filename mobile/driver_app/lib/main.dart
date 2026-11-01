import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import 'package:map_kit/map_kit.dart';

import 'core/config.dart';
import 'services/driver_map_integration.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await MapEnv.load(fileName: '.env');
  runApp(const DriverApp());
}

class DriverApp extends StatelessWidget {
  const DriverApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Driver — Emergency Ambulance',
      theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0EA5E9)),
      home: const DriverDashboard(),
    );
  }
}

class DriverDashboard extends StatefulWidget {
  const DriverDashboard({super.key});

  @override
  State<DriverDashboard> createState() => _DriverDashboardState();
}

class _DriverDashboardState extends State<DriverDashboard> {
  bool online = false;
  String? demoEmergencyId;

  @override
  void initState() {
    super.initState();
    _ensureLocation();
  }

  Future<void> _ensureLocation() async {
    await LocationService.instance.ensurePermission();
  }

  Future<void> _startDemoNavigation() async {
    final pos = await Geolocator.getCurrentPosition();
    final patient = LatLng(pos.latitude + 0.008, pos.longitude + 0.008);
    demoEmergencyId ??= '00000000-0000-0000-0000-000000000001';
    if (!mounted) return;
    await DriverMapIntegration.openNavigation(
      context: context,
      emergencyId: demoEmergencyId!,
      patientLocation: patient,
    );
  }

  @override
  void dispose() {
    DriverMapIntegration.stopGps();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Driver Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.map),
            onPressed: () => DriverMapIntegration.openFleetMap(context),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          SwitchListTile(
            title: const Text('Online / Available'),
            subtitle: const Text('Uses OpenStreetMap + OSRM routing'),
            value: online,
            onChanged: (v) => setState(() => online = v),
          ),
          Card(
            color: const Color(0xFFFEE2E2),
            child: ListTile(
              leading: const Icon(Icons.emergency, color: Color(0xFFDC2626)),
              title: const Text('Active Emergency Request'),
              subtitle: const Text('Accept to open live Mapbox route'),
              trailing: FilledButton(
                onPressed: online ? _startDemoNavigation : null,
                child: const Text('Navigate'),
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Row(
            children: [
              Expanded(child: _StatCard(title: 'Today Earnings', value: '₹0')),
              SizedBox(width: 12),
              Expanded(child: _StatCard(title: 'Trips', value: '0')),
            ],
          ),
          const SizedBox(height: 16),
          ListTile(
            leading: const Icon(Icons.navigation),
            title: const Text('OSRM Navigation'),
            subtitle: const Text('Free emergency routes via OpenStreetMap routing'),
            onTap: _startDemoNavigation,
          ),
          ListTile(
            leading: const Icon(Icons.wifi_tethering),
            title: const Text('WebSocket GPS Broadcast'),
            subtitle: const Text('POST /emergencies/{id}/gps/ every 5s'),
          ),
          ListTile(
            leading: const Icon(Icons.offline_bolt),
            title: const Text('Offline OSM Tile Cache'),
            subtitle: const Text('Cached OpenStreetMap tiles for low bandwidth'),
          ),
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  const _StatCard({required this.title, required this.value});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text(title, style: const TextStyle(fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
