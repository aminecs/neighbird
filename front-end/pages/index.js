import Head from 'next/head';
import React from 'react';
import data from '../../data/example_topics_metrics.json';

const Home = () => {
  const hotTopics = data.slice(0, 11);
  return (
    <div className="flex flex-col items-center w-screen h-full">
      <Head>
        <title>#Codechella Team - Bird Bot</title>
      </Head>
      <h1 className="text-5xl font-bold mb-20">#Codechella Bird Bot</h1>
      <div className="w-full max-w-4xl">
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
