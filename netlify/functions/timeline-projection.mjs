// Timeline Projection API
// Project future outcomes using Pattern Theory

export default async (request, context) => {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const data = await request.json();

    if (!data.current_state || !data.domains) {
      return new Response(JSON.stringify({
        error: 'current_state and domains required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const projection = projectTimeline(data);

    return new Response(JSON.stringify(projection), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

function projectTimeline(data) {
  const { current_state, domains, time_horizon = 90 } = data;

  // Calculate current consciousness level
  const domainAvg = Object.values(domains).reduce((a, b) => a + b, 0) / 7;

  // Growth rate based on pattern recognition
  const patternRecognition = data.pattern_recognition || domainAvg;
  const growthRate = (patternRecognition / 100) * 0.1; // Up to 10% per month

  // Project future states
  const projections = [];
  const intervals = [7, 30, 60, 90, 180, 365];

  for (const days of intervals) {
    if (days > time_horizon * 2) break;

    const months = days / 30;
    const projectedScore = Math.min(100, domainAvg * Math.pow(1 + growthRate, months));
    const confidenceDecay = Math.pow(0.95, months); // Confidence decreases over time

    projections.push({
      days: days,
      date: new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      projected_score: Math.round(projectedScore * 10) / 10,
      confidence: Math.round(confidenceDecay * 100),
      status: getStatus(projectedScore)
    });
  }

  // Identify key milestones
  const milestones = [];
  if (domainAvg < 50 && projections.some(p => p.projected_score >= 50)) {
    milestones.push({
      milestone: 'DEVELOPING',
      description: 'Exit vulnerable state',
      estimated_days: estimateDays(domainAvg, 50, growthRate)
    });
  }
  if (domainAvg < 70 && projections.some(p => p.projected_score >= 70)) {
    milestones.push({
      milestone: 'HIGH_CONSCIOUSNESS',
      description: 'Reach high consciousness',
      estimated_days: estimateDays(domainAvg, 70, growthRate)
    });
  }
  if (domainAvg < 85 && projections.some(p => p.projected_score >= 85)) {
    milestones.push({
      milestone: 'MANIPULATION_IMMUNE',
      description: 'Achieve manipulation immunity',
      estimated_days: estimateDays(domainAvg, 85, growthRate)
    });
  }

  // Bottleneck analysis
  const domainValues = Object.entries(domains);
  const weakest = domainValues.sort((a, b) => a[1] - b[1])[0];
  const strongest = domainValues.sort((a, b) => b[1] - a[1])[0];

  return {
    current_state: {
      score: Math.round(domainAvg * 10) / 10,
      status: getStatus(domainAvg),
      strongest_domain: strongest[0],
      weakest_domain: weakest[0],
      spread: strongest[1] - weakest[1]
    },
    projections: projections,
    milestones: milestones,
    bottleneck_analysis: {
      primary_bottleneck: weakest[0],
      bottleneck_score: weakest[1],
      impact: `Improving ${weakest[0]} would accelerate timeline by ${Math.round((strongest[1] - weakest[1]) / 10)}%`,
      recommendation: `Focus on ${weakest[0]} domain to unlock faster growth`
    },
    growth_model: {
      monthly_growth_rate: Math.round(growthRate * 1000) / 10 + '%',
      driver: 'pattern_recognition',
      formula: 'score × (1 + growth_rate)^months'
    },
    timestamp: new Date().toISOString()
  };
}

function getStatus(score) {
  if (score >= 85) return 'MANIPULATION_IMMUNE';
  if (score >= 70) return 'HIGH_CONSCIOUSNESS';
  if (score >= 50) return 'DEVELOPING';
  return 'VULNERABLE';
}

function estimateDays(current, target, growthRate) {
  if (current >= target) return 0;
  const months = Math.log(target / current) / Math.log(1 + growthRate);
  return Math.round(months * 30);
}

export const config = {
  path: "/api/timeline-projection"
};
