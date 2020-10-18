import React, { useState } from 'react';
import { atom } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './camera.scss';


export const cameraState = atom({
	key: 'camera',
	default: {
		fetched: false,
		error: undefined
	}
});

const Camera = () => {
	useAPIPoll(cameraState, '/camera/ping', 60000);
	const [isLoading, setIsLoading] = useState(true);

	const innerSrc = window.jsData.demoMode ? '/static/closeup.jpg' : `${window.location.origin}:8081`;

	return (
		<div className="panel is-info camera">
			<div className="panel-heading">Cameras</div>
			<div className="panel-block inside">
				<div className={`video-container ${isLoading ? 'loader' : ''}`}>
					<img 
						src={innerSrc} 
						onLoad={() => { 
							if (isLoading) { 
								setIsLoading(false)
							}
						}}
						onError={(err) => {
							if (!isLoading) {
								console.error(err);
								setIsLoading(true);
							}
						}}
						alt="Inside coop camera"
					/>
				</div>
			</div>
		</div>
	);
};

export default Camera;
