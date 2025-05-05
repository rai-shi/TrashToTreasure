import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Card, Spinner, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import projectService from '../../services/projectService';

// Custom node component for roadmap steps
const RoadmapStepNode = React.memo(({ data }) => {
  const { step_number, title, description, estimated_time, materials_needed = [] } = data;
  
  return (
    <Card className="shadow-sm border-0" style={{ width: 280, maxWidth: '100%' }}>
      <Card.Body className="p-3">
        <div className="d-flex align-items-center mb-2">
          <div className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center me-2" 
               style={{ width: 24, height: 24, minWidth: 24 }}>
            {step_number}
          </div>
          <Card.Title className="fs-6 mb-0">{title || 'Untitled Step'}</Card.Title>
        </div>
        <Card.Text className="small text-muted mb-2">
          {description ? (
            description.length > 100 ? `${description.substring(0, 100)}...` : description
          ) : 'No description available'}
        </Card.Text>
        <div className="d-flex flex-column gap-2">
          <span className="badge bg-info text-dark d-flex align-items-center gap-1">
            <i className="fas fa-clock"></i>
            {estimated_time || 'Time not specified'}
          </span>
          <span className="badge bg-secondary d-flex align-items-center gap-1">
            <i className="fas fa-tools"></i>
            {materials_needed.length ? `${materials_needed.length} materials` : 'No materials specified'}
          </span>
        </div>
      </Card.Body>
    </Card>
  );
});

// Define nodeTypes outside component to prevent recreation on each render
const nodeTypes = {
  roadmapStep: RoadmapStepNode,
};

const ProjectRoadmap = ({ projectId }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [roadmapData, setRoadmapData] = useState(null);
  const navigate = useNavigate();

  // Wrapper styles with fixed dimensions
  const wrapperStyles = {
    width: '100%',
    height: '600px',
    marginBottom: '2rem',
    border: '1px solid #eee',
    borderRadius: '8px',
    overflow: 'hidden'
  };

  // Layout calculation for nodes
  const calculateLayout = useCallback((steps) => {
    if (!Array.isArray(steps) || steps.length === 0) {
      console.warn('Invalid or empty steps array');
      return { nodes: [], edges: [] };
    }

    const nodeGap = 300;  // Gap between nodes
    const newNodes = [];
    const newEdges = [];
    
    steps.forEach((step, index) => {
      // Ensure step has required fields
      const validStep = {
        id: step.id,
        step_number: step.step_number || index + 1,
        title: step.title || `Step ${index + 1}`,
        description: step.description || '',
        estimated_time: step.estimated_time || '',
        materials_needed: Array.isArray(step.materials_needed) ? step.materials_needed : []
      };

      // Create node with zigzag layout for better visual flow
      const yOffset = index % 2 === 0 ? 0 : 100;
      const nodeId = `step-${validStep.id}`;
      newNodes.push({
        id: nodeId,
        type: 'roadmapStep',
        position: { x: index * nodeGap, y: yOffset },
        data: validStep,
        draggable: false,
        selectable: false
      });
      
      // Create edge to next node
      if (index < steps.length - 1) {
        const nextId = `step-${steps[index + 1].id}`;
        newEdges.push({
          id: `edge-${nodeId}-${nextId}`,
          source: nodeId,
          target: nextId,
          type: 'smoothstep',
          animated: true,
          style: { stroke: '#28a745', strokeWidth: 2 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: '#28a745',
          },
        });
      }
    });
    
    return { nodes: newNodes, edges: newEdges };
  }, []);

  useEffect(() => {
    const fetchRoadmap = async () => {
      if (!projectId) {
        console.log('[DEBUG] No project ID provided');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError('');
      
      try {
        console.log('[DEBUG] Fetching roadmap for project:', projectId);
        const roadmapSteps = await projectService.getProjectRoadmap(projectId);
        console.log('[DEBUG] Received roadmap steps:', roadmapSteps);
        
        if (!Array.isArray(roadmapSteps)) {
          throw new Error('Invalid roadmap data received');
        }

        setRoadmapData(roadmapSteps);
        
        const { nodes: layoutNodes, edges: layoutEdges } = calculateLayout(roadmapSteps);
        console.log('[DEBUG] Calculated layout:', { nodes: layoutNodes.length, edges: layoutEdges.length });
        
        setNodes(layoutNodes);
        setEdges(layoutEdges);
      } catch (err) {
        console.error('[ERROR] Failed to fetch roadmap:', err);
        
        // Handle session expiration
        if (err.message === 'Your session has expired. Please login again.') {
          setError('Your session has expired. Redirecting to login...');
          setTimeout(() => {
            navigate('/login');
          }, 2000);
          return;
        }
        
        setError(err.message || 'Failed to load the project roadmap. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchRoadmap();
  }, [projectId, calculateLayout, navigate]);

  if (loading) {
    return (
      <div className="text-center p-5">
        <Spinner animation="border" variant="success" />
        <p className="mt-2">Loading roadmap...</p>
      </div>
    );
  }
  
  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <div style={wrapperStyles}>
      {nodes.length === 0 ? (
        <div className="d-flex align-items-center justify-content-center h-100">
          <Alert variant="info" className="m-0">
            No roadmap steps available. Please generate a roadmap first.
          </Alert>
        </div>
      ) : (
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ 
            padding: 0.3,
            includeHiddenNodes: true,
            minZoom: 0.5,
            maxZoom: 2
          }}
          minZoom={0.2}
          maxZoom={2}
          defaultViewport={{ x: 0, y: 0, zoom: 0.8 }}
          zoomOnScroll={false}
          panOnScroll={true}
          selectionOnDrag={false}
          panOnDrag={[1, 2]}
          style={{ width: '100%', height: '100%' }}
        >
          <Controls 
            position="bottom-right"
            style={{ margin: '1rem' }}
            showInteractive={false}
          />
          <MiniMap 
            nodeStrokeColor="#28a745"
            nodeColor="#fff"
            nodeBorderRadius={4}
            position="bottom-left"
            style={{ margin: '1rem' }}
            maskColor="rgba(248, 249, 250, 0.8)"
          />
          <Background 
            variant="dots" 
            gap={16} 
            size={1} 
            color="rgba(40, 167, 69, 0.1)"
          />
        </ReactFlow>
      )}
    </div>
  );
};

export default ProjectRoadmap; 