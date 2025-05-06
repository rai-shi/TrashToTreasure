// components/project/ProjectRoadmap.js
import React from 'react';
import './ProjectRoadmap.css';

const ProjectRoadmap = ({ roadmap }) => {
  if (!roadmap || roadmap.length === 0) {
    return <p>Yol haritası verisi bulunamadı.</p>;
  }

  return (
    <div className="timeline-container">
      {roadmap.map((step, index) => (
        <div className="timeline-item" key={index}>
          <div className="timeline-marker">
            <span className="timeline-number">{index + 1}</span>
            {index !== roadmap.length - 1 && <div className="timeline-line"></div>}
          </div>
          <div className="timeline-content">
            <p>{step}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProjectRoadmap;
