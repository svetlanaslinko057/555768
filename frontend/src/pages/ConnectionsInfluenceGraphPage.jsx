/**
 * ConnectionsInfluenceGraphPage
 * 
 * Graph visualization for Twitter influencer relationships.
 * Uses existing RouteGraphView component (same as Graph Intelligence → Routes)
 * 
 * This page is under Connections → Graph submenu
 */

import { useState, useCallback, useRef } from 'react';
import { Network, RefreshCw, Filter, Download, Users } from 'lucide-react';
import { Link } from 'react-router-dom';
import ForceGraphCore from '../graph/core/ForceGraphCore';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

/**
 * ConnectionsInfluenceGraphPage - влияние между Twitter инфлюенсерами
 */
export default function ConnectionsInfluenceGraphPage() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const containerRef = useRef(null);

  // Fetch graph from Connections API
  const fetchGraph = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${BACKEND_URL}/api/connections/graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ limit_nodes: 50 }),
      });
      const data = await res.json();
      
      if (data.ok && data.data) {
        setGraphData({
          nodes: data.data.nodes.map(n => ({
            id: n.id,
            label: n.label,
            displayName: n.label,
            profile: n.profile,
            influence_score: n.influence_score,
            early_signal: n.early_signal,
            risk_level: n.risk_level,
            color: n.color,
            val: n.size || 15,
          })),
          links: data.data.edges.map(e => ({
            id: e.id,
            source: e.source,
            target: e.target,
            from: e.source,
            to: e.target,
            direction: e.direction === 'outbound' ? 'OUT' : e.direction === 'inbound' ? 'IN' : 'BOTH',
            weight: e.weight,
          })),
        });
      }
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  }, []);

  // Load on mount
  useState(() => {
    fetchGraph();
  }, []);

  // Handle node click
  const handleNodeClick = useCallback((node) => {
    setSelectedNode(node);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-[1600px] mx-auto px-4 py-4">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center">
                <Network className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Connections Graph</h1>
                <p className="text-sm text-gray-500">Twitter Influencer Relationships</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={fetchGraph}
                disabled={loading}
                className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm hover:bg-gray-50"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            </div>
          </div>
        </div>

        {/* Sub-navigation tabs */}
        <div className="flex items-center gap-2 mb-6">
          <Link
            to="/connections"
            className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <span className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Influencers
            </span>
          </Link>
          <span className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-900 text-white">
            <span className="flex items-center gap-2">
              <Network className="w-4 h-4" />
              Graph
            </span>
          </span>
        </div>

        {/* Stats bar */}
        <div className="flex items-center gap-4 mb-4 p-3 bg-white border border-gray-200 rounded-xl">
          <span className="text-sm">
            <strong>{graphData.nodes.length}</strong> nodes
          </span>
          <span className="text-gray-300">|</span>
          <span className="text-sm">
            <strong>{graphData.links.length}</strong> edges
          </span>
          {selectedNode && (
            <>
              <span className="text-gray-300">|</span>
              <span className="text-sm text-indigo-600">
                Selected: <strong>{selectedNode.label}</strong>
              </span>
            </>
          )}
        </div>

        {/* Graph Container */}
        <div 
          ref={containerRef} 
          className="bg-[#0a0e1a] rounded-xl overflow-hidden" 
          style={{ height: 600 }}
        >
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <RefreshCw className="w-8 h-8 text-gray-400 animate-spin" />
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center h-full text-red-400">
              <span>{error}</span>
              <button onClick={fetchGraph} className="mt-2 text-sm underline">
                Retry
              </button>
            </div>
          ) : (
            <ForceGraphCore
              data={graphData}
              width={1560}
              height={600}
              onNodeClick={handleNodeClick}
              selectedNodeId={selectedNode?.id}
              fitOnLoad={true}
            />
          )}
        </div>

        {/* Legend */}
        <div className="mt-4 flex items-center justify-between p-3 bg-white border border-gray-200 rounded-xl text-xs">
          <div className="flex items-center gap-6">
            <span className="font-semibold text-gray-500 uppercase">Node Colors:</span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-gray-600">Breakout</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-yellow-500" />
              <span className="text-gray-600">Rising</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-indigo-500" />
              <span className="text-gray-600">Whale</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-purple-500" />
              <span className="text-gray-600">Influencer</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-gray-500" />
              <span className="text-gray-600">Retail</span>
            </span>
          </div>
        </div>
      </main>
    </div>
  );
}
