import {
  ArrowDownIcon,
  ArrowUpIcon,
  EyeOffIcon,
  EyeOpenIcon,
  InfoSignIcon,
  MaximizeIcon,
  Popover,
} from 'evergreen-ui';
import Head from 'next/head';
import React, { useEffect, useState } from 'react';
import { ComposableMap, Geographies, Geography, Marker, ZoomableGroup } from 'react-simple-maps';
import mapData from '../../data/example_community_long_lat_metrics.json';
import data from '../../data/example_topics_metrics.json';
import { Canada, Nigeria, Scottland, USA } from '../components/icons/flags';
import Logo from '../components/icons/logo';

const geoUrl =
  'https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json';

const team = [
  {
    name: 'Teleayo Oyekunle',
    role: 'Back-End Developer',
    flag: <Nigeria />,
    image: '/images/Ellipse 13.png',
  },
  {
    name: 'Nnaji Obinelo',
    role: 'Back-End Developer',
    flag: <USA />,
    image: '/images/Ellipse 14.png',
  },
  {
    name: 'Mohamed Amine Belabbes',
    role: 'Back-End Developer',
    flag: <Scottland />,
    image: '/images/Ellipse 15.png',
  },
  {
    name: 'Ogheneochuko Pedro',
    role: 'Front-End Developer',
    flag: <Nigeria />,
    image: '/images/Ellipse 16.png',
  },
  {
    name: 'Janice Cheung',
    role: 'UX Designer',
    flag: <Canada />,
    image: '/images/Ellipse 17.png',
  },
];

const Home = () => {
  const hotTopics = data.slice(0, 11);

  const [coordinates, setCoordinate] = useState([0, 0]);
  const [zoom, setZoom] = useState(1);
  const [position, setPosition] = useState({ coordinates: [0, 0], zoom: 1 });
  const [hotTopicsPag, setHotTopicsPag] = useState(2);
  const [showHotTopics, setShowHotTopics] = useState(true);
  const [selectedCommunity, setSelectedCommunity] = useState(null);
  const [showSelectedCommunity, setShowSelectedCommunity] = useState(null);
  const [communityDetails, setCommunityDetails] = useState(true);

  function handleMoveEnd(position) {
    setPosition(position);
  }

  useEffect(() => {
    window.innerWidth <= 600 && setShowHotTopics(false);
  });

  return (
    <div
      className="flex flex-col items-center w-full h-full overflow-hidden relative"
      style={{ backgroundColor: '#000' }}
    >
      <Head>
        <title>The Neighbird - #Codechella</title>
        <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico" />
      </Head>
      <div className="flex flex-col items-center w-full h-screen overflow-hidden relative" id="app">
        <div className="flex px-5 py-2 w-full items-center">
          <Logo />
          <div className="flex flex-col ml-5">
            <div className="flex items-center">
              <p className="text-white text-xl font-bold">The Neighbird</p>&nbsp;&nbsp;
              <a
                href="https://twitter.com/theneighbird"
                target="_blank"
                rel="noreferrer"
                className="text-gray-600 hover:text-primaryColor"
                // style={{ color: '#828282' }}
              >
                @theneighbird
              </a>
            </div>
            <p className="text-primaryColor font-bold text-xl">around the world</p>
          </div>
        </div>
        <div className="w-full h-full relative">
          <div className="h-full w-full" style={{ backgroundColor: '#191A1A' }}>
            <ComposableMap height={600} width={1000}>
              <ZoomableGroup
                zoom={zoom}
                center={coordinates}
                fill="#1d9be8"
                strokeWidth="10px"
                onMoveEnd={handleMoveEnd}
              >
                <Geographies geography={geoUrl}>
                  {({ geographies }) =>
                    geographies.map((geo, index) => {
                      console.log(geo.properties.NAME);
                      return (
                        <Geography
                          fill="#343332"
                          stroke="white"
                          strokeWidth="0.1px"
                          key={geo.rsmKey}
                          geography={geo}
                        />
                      );
                    })
                  }
                </Geographies>
                {mapData
                  .sort((a, b) => (b.bot_usage_count > a.bot_usage_count ? 1 : -1))
                  .map((city, index) => {
                    return (
                      <Marker
                        key={city.city + index}
                        coordinates={city.location}
                        onClick={() => {
                          setSelectedCommunity(city);
                          setCoordinate(city.location);
                          setZoom(4);
                          setShowSelectedCommunity(true);
                        }}
                      >
                        <Popover
                          content={
                            <div className="flex p-2">
                              <p className="font-semibold">{city.city}</p>,&nbsp;
                              <p>{city.country}</p>
                            </div>
                          }
                          trigger="hover"
                        >
                          <circle
                            r={city.bot_usage_count / 7}
                            fill="#1DA1F2"
                            stroke="#fff"
                            strokeWidth={
                              showSelectedCommunity && selectedCommunity.city !== city.city
                                ? '0.1'
                                : '0.5'
                            }
                            className={`cursor-pointer ${
                              showSelectedCommunity &&
                              selectedCommunity.city !== city.city &&
                              'opacity-50'
                            }`}
                            tooltip={city.city}
                          />
                        </Popover>
                      </Marker>
                    );
                  })}
              </ZoomableGroup>
            </ComposableMap>
          </div>
          <div
            className={`absolute right-0 top-0 mr-5 mt-5 ${
              !communityDetails && !showHotTopics ? 'w-12' : 'w-72'
            }`}
          >
            <div
              className={`w-full border-2 border-white rounded mb-5 ${!showHotTopics && 'w-16'}`}
            >
              <div
                className={`flex justify-between items-center py-4 border-b px-3 text-primaryColor ${
                  !showHotTopics && showHotTopics && 'w-10'
                }`}
                style={{ backgroundColor: '#15181C' }}
              >
                <p className={`text-lg font-bold text-white ${!showHotTopics && 'hidden'}`}>
                  Trending Worldwide
                </p>
                {showHotTopics ? (
                  <EyeOpenIcon
                    size={20}
                    className="cursor-pointer"
                    onClick={() => setShowHotTopics(false)}
                  />
                ) : (
                  <EyeOffIcon
                    size={20}
                    className="cursor-pointer"
                    onClick={() => setShowHotTopics(true)}
                  />
                )}
              </div>
              <div className={`w-full h-72 overflow-auto ${!showHotTopics && 'hidden'}`}>
                {hotTopics.slice(0, hotTopicsPag + 1).map((topic, index) => {
                  return (
                    <div
                      key={topic.topic + index}
                      style={{ backgroundColor: '#15181C', borderTop: '0.1px gray solid' }}
                      className="p-2 px-3 hover:bg-opacity-50"
                    >
                      <p className="text-gray-500 text-sm">Trending Worldwide</p>
                      <p className="text-white">{topic.topic}</p>
                      <p className="text-gray-500 text-sm">{topic.bot_usage_count} Requests</p>
                    </div>
                  );
                })}
                <div
                  style={{ backgroundColor: '#15181C', borderTop: '0.1px gray solid' }}
                  className="pt-2 px-3 h-11 hover:bg-opacity-50"
                >
                  <p
                    className={`text-primaryColor cursor-pointer ${
                      hotTopicsPag >= hotTopics.length && 'hidden'
                    }`}
                    onClick={() => setHotTopicsPag(hotTopicsPag + 3)}
                  >
                    Show more
                  </p>
                </div>
              </div>
            </div>
            {showSelectedCommunity && (
              <div
                className={`w-full border-2 border-white rounded ${!communityDetails && 'w-12'}`}
              >
                <div
                  className={`flex justify-between items-center py-4 border-b px-3 text-primaryColor ${
                    !showSelectedCommunity && 'hidden'
                  }`}
                  style={{ backgroundColor: '#15181C' }}
                >
                  <p className={`text-lg font-bold text-white ${!communityDetails && 'hidden'}`}>
                    {selectedCommunity.city}
                  </p>
                  {
                    <InfoSignIcon
                      className="cursor-pointer"
                      onClick={() => setCommunityDetails(!communityDetails)}
                    />
                  }
                </div>
                <div className={`w-full overflow-auto ${!communityDetails && 'hidden'}`}>
                  <div
                    style={{ backgroundColor: '#15181C', borderTop: '0.1px gray solid' }}
                    className="p-2 px-3 hover:bg-opacity-50"
                  >
                    <p className="text-gray-500 text-sm">Users Currently Active</p>
                    <p className="text-white">{selectedCommunity.bot_usage_count}</p>
                  </div>
                  <div
                    style={{ backgroundColor: '#15181C', borderTop: '0.1px gray solid' }}
                    className="p-2 px-3 hover:bg-opacity-50"
                  >
                    <p className="text-gray-500 text-sm">Topic · Trending</p>
                    <p className="text-white">{selectedCommunity.topic}</p>
                  </div>
                  <div
                    style={{ backgroundColor: '#15181C', borderTop: '0.1px gray solid' }}
                    className="p-2 px-3 hover:bg-opacity-50"
                  >
                    <p className="text-gray-500 text-sm">Users · Who Have Used BirdBot</p>
                    <p className="text-white">{selectedCommunity.bot_usage_count * 21}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        <div className="absolute bottom-0 right-0 mb-5 mr-5 flex flex-col reltaive">
          <p
            className={`rounded-sm bg-white p-2 text-2xl font-bold mb-2 cursor-pointer ${
              !showSelectedCommunity && 'hidden'
            }`}
          >
            <MaximizeIcon
              onClick={() => {
                setShowSelectedCommunity(false);
                setSelectedCommunity(null);
                setZoom(1);
                setCoordinate([0, 0]);
              }}
              size={20}
            />
          </p>
          <p
            className="rounded-sm bg-white px-2 text-2xl font-bold mb-2 cursor-pointer text-center"
            onClick={() => {
              if (zoom !== 8) setZoom(zoom + 1);
            }}
          >
            +
          </p>
          <p
            className="rounded-sm bg-white px-2 text-2xl font-bold cursor-pointer text-center"
            onClick={() => {
              if (zoom !== 1) setZoom(zoom - 1);
              setShowSelectedCommunity(false);
              setSelectedCommunity(null);
            }}
          >
            -
          </p>
        </div>
        <div className="absolute bottom-0 left-0 mb-5 ml-5 flex flex-col reltaive text-white">
          <a className="flex items-center cursor-pointer" href="#team">
            Power Of 5 &nbsp;
            <ArrowDownIcon />
          </a>
        </div>
      </div>
      <div
        className="flex flex-col items-center justify-center tablet:my-auto tablet:overflow-y-auto tablet:justify-start w-full h-screen overflow-hidden relative"
        id="team"
      >
        <div className="w-full flex flex-col items-center justify-center max-w-7xl">
          <div className="flex px-5 py-2 mb-20 w-full items-center flex-wrap">
            <Logo className="w-56 h-56 mb-12" />
            <div className="flex flex-col ml-5 tablet:ml-0">
              <p className="text-white font-bold text-8xl phone:text-7xl">The Neighbird</p>
              &nbsp;&nbsp;
              <a
                href="https://twitter.com/theneighbird"
                target="_blank"
                rel="noreferrer"
                className="text-gray-600 text-3xl justify-self-end hover:text-primaryColor"
                // style={{ color: '#828282' }}
              >
                @theneighbird
              </a>
            </div>
            <div className="flex flex-col ml-16 items-between tablet:mt-10 tablet:ml-0">
              <div>
                <p className="text-primaryColor text-3xl">#Codechella Hackathon</p>
                <p className="text-primaryColor text-3xl">November 18 - 22, 2020</p>
              </div>
              <p className="text-white text-3xl mt-8">Team Name: Power of 5</p>
            </div>
          </div>
          <div className="flex justify-around w-full flex-wrap">
            {team.map((mate, index) => {
              return (
                <div className="flex flex-col items-center mb-10">
                  <img src={mate.image} className="w-48 mb-9" />
                  {mate.flag}
                  <p className="text-white font-bold text-xl mt-3">{mate.name}</p>
                  <p className="text-primaryColor font-bold text-xl mt-3">{mate.role}</p>
                </div>
              );
            })}
          </div>
        </div>
        <div className="absolute bottom-0 left-0 mb-5 ml-5 flex flex-col reltaive text-white">
          <a className="flex items-center cursor-pointer tablet:flex" href="#app">
            Back to App &nbsp;
            <ArrowUpIcon />
          </a>
        </div>
      </div>
    </div>
  );
};

export default Home;
