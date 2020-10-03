import React from 'react';
import { atom, useRecoilValue } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './pi.scss';


export const piState = atom({
	key: 'pi',
	default: {
		fetched: false,
		error: undefined,
		temperatureFahrenheit: undefined,
		uptime: undefined,
		memoryPercent: undefined,
		swapPercent: undefined,
		loadAverages: [undefined, undefined, undefined],
	},
});

const Pi = () => {
	useAPIPoll(piState, '/pi/status', 7000);
	const pi = useRecoilValue(piState);
	
	return (
		<div className="panel is-link pi">
			<div className="panel-heading">Pi</div>
			<div className="panel-block temperature">Temperature: { pi.temperatureFahrenheit }°F</div>
			<div className="panel-block uptime">Uptime: { pi.uptime }</div>
			<div className="panel-block memory-percent">Memory usage: { pi.memoryPercent }%</div>
			<div className="panel-block swap-percent">Swap usage: { pi.swapPercent }%</div>
			<div className="panel-block load-averages">Load: { pi.loadAverages + '' }</div>
		</div>
	);
};

export default Pi;
