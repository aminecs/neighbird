import Head from 'next/head';
import React, { useState } from 'react';
import { ComposableMap, Geographies, Geography, ZoomableGroup } from 'react-simple-maps';
import data from '../../data/example_topics_metrics.json';

const geoUrl =
  'https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json';

const Home = () => {
  const hotTopics = data.slice(0, 11);

  const [position, setPosition] = useState({ coordinates: [0, 0], zoom: 1 });

  function handleMoveEnd(position) {
    setPosition(position);
  }

  return (
    <div className="flex flex-col items-center w-full h-full">
      <Head>
        <title>#Codechella Team - Bird Bot</title>
      </Head>
      <h1 className="text-5xl font-bold my-20">#Codechella Bird Bot</h1>
      {/* <WorldMap /> */}
      <div className="w-full px-20 tablet:px-10 phone:px-5">
        <div className="border-2 rounded border-gray-300 mb-20">
          <ComposableMap width="1000" height="500">
            <ZoomableGroup
              zoom={position.zoom}
              center={position.coordinates}
              fill="#1d9be8"
              strokeWidth="5px"
              onMoveEnd={handleMoveEnd}
            >
              <Geographies geography={geoUrl}>
                {({ geographies }) =>
                  geographies.map((geo) => <Geography key={geo.rsmKey} geography={geo} />)
                }
              </Geographies>
            </ZoomableGroup>
          </ComposableMap>
        </div>
        <p className="text-2xl mb-5 text-red-500 font-semibold">Hot Topics ‎️‍🔥</p>
        <ul className="list-decimal ml-5">
          {hotTopics
            .sort((a, b) => (b.bot_usage_count > a.bot_usage_count ? 1 : -1))
            .map((topic, index) => (
              <li key={topic.topic + index}>
                {topic.topic} - {topic.bot_usage_count} requests
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
};

export default Home;
