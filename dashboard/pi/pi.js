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
			<div className="panel-block temperature">
				<span className="key">Temperature:</span>&nbsp;<span className="value">{ pi.temperatureFahrenheit }°F</span>
			</div>
			<div className="panel-block uptime">
				<span className="key">Uptime:</span>&nbsp;<span className="value">{ pi.uptime }</span>
			</div>
			<div className="panel-block memory-percent">
				<span className="key">Memory usage:</span>&nbsp;<span className="value">{ pi.memoryPercent }%</span>
			</div>
			<div className="panel-block swap-percent">
				<span className="key">Swap usage:</span>&nbsp;<span className="value">{ pi.swapPercent }%</span>
			</div>
			<div className="panel-block load-averages">
				<span className="key">Load:</span>&nbsp;<span className="value">{ pi.loadAverages + '' }</span>
			</div>
		</div>
	);
};

export default Pi;
